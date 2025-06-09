from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from ultralytics import YOLO
import cv2
import os
import json
from datetime import datetime
import numpy as np
from collections import Counter
import threading
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'
MODEL_PATH = 'models/yolov8n.pt'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm'}

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# Global variables for processing status
processing_status = {}
processing_results = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def analyze_video_with_yolo(video_path, task_id, threshold=20):
    """
    Analyze video using YOLO model and return comprehensive results
    """
    try:
        model = YOLO(MODEL_PATH)
        cap = cv2.VideoCapture(video_path)
        
        # Initialize counters and lists
        frame_count = 0
        total_people_per_frame = []
        all_detected_objects = []
        max_people_in_frame = 0
        alert_frames = 0
        
        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        processing_status[task_id] = {
            'status': 'processing',
            'progress': 0,
            'message': 'Starting video analysis...'
        }
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # Update progress
            progress = int((frame_count / total_frames) * 100)
            processing_status[task_id]['progress'] = progress
            processing_status[task_id]['message'] = f'Processing frame {frame_count}/{total_frames}'
            
            # Run YOLO detection
            results = model(frame, verbose=False)
            
            if len(results[0].boxes) > 0:
                class_ids = results[0].boxes.cls.cpu().numpy().astype(int)
                class_names = model.names
                detected_objects = [class_names[c] for c in class_ids]
                
                # Count people
                person_count = detected_objects.count('person')
                total_people_per_frame.append(person_count)
                
                # Track max people
                if person_count > max_people_in_frame:
                    max_people_in_frame = person_count
                
                # Check for crowd alert
                if person_count > threshold:
                    alert_frames += 1
                
                # Store all detected objects
                all_detected_objects.extend(detected_objects)
            else:
                total_people_per_frame.append(0)
        
        cap.release()
        
        # Calculate statistics
        avg_people = np.mean(total_people_per_frame) if total_people_per_frame else 0
        total_people = max(total_people_per_frame) if total_people_per_frame else 0
        
        # Count different object types
        object_counts = Counter(all_detected_objects)
        
        # Calculate crowd density (as percentage of maximum detected)
        crowd_density = min(100, int((avg_people / max(1, max_people_in_frame)) * 100))
        
        # Determine safety level
        if crowd_density > 70 or max_people_in_frame > threshold * 1.5:
            safety_level = "High Risk"
        elif crowd_density > 50 or max_people_in_frame > threshold:
            safety_level = "Medium Risk"
        else:
            safety_level = "Safe"
        
        # Calculate confidence (based on detection consistency)
        confidence = min(95, max(75, 100 - int(np.std(total_people_per_frame) * 2)))
        
        # Prepare results
        results_data = {
            'total_people': int(total_people),
            'avg_people': round(avg_people, 1),
            'max_people': int(max_people_in_frame),
            'crowd_density': crowd_density,
            'safety_level': safety_level,
            'confidence': confidence,
            'vehicle_count': object_counts.get('car', 0) + object_counts.get('truck', 0) + object_counts.get('bus', 0),
            'bag_count': object_counts.get('backpack', 0) + object_counts.get('handbag', 0) + object_counts.get('suitcase', 0),
            'suspicious_objects': object_counts.get('knife', 0) + object_counts.get('gun', 0),
            'all_objects': dict(object_counts),
            'alert_frames': alert_frames,
            'total_frames': total_frames,
            'video_duration': round(total_frames / fps, 2) if fps > 0 else 0,
            'processed_at': datetime.now().isoformat()
        }
        
        # Store results
        processing_results[task_id] = results_data
        processing_status[task_id] = {
            'status': 'completed',
            'progress': 100,
            'message': 'Video analysis completed successfully!'
        }
        
    except Exception as e:
        processing_status[task_id] = {
            'status': 'error',
            'progress': 0,
            'message': f'Error processing video: {str(e)}'
        }

@app.route('/')
def index():
    return jsonify({"message": "Crowd Management API is running!"})

@app.route('/upload', methods=['POST'])
def upload_video():
    try:
        if 'video' not in request.files:
            return jsonify({'error': 'No video file provided'}), 400
        
        file = request.files['video']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            # Generate unique filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{file.filename}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            
            # Save file
            file.save(filepath)
            
            # Generate task ID
            task_id = f"task_{timestamp}"
            
            # Start processing in background thread
            thread = threading.Thread(
                target=analyze_video_with_yolo,
                args=(filepath, task_id, 20)  # threshold = 20
            )
            thread.start()
            
            return jsonify({
                'message': 'Video uploaded successfully',
                'task_id': task_id,
                'filename': filename
            })
        else:
            return jsonify({'error': 'Invalid file format'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/status/<task_id>')
def get_status(task_id):
    try:
        if task_id in processing_status:
            return jsonify(processing_status[task_id])
        else:
            return jsonify({'error': 'Task not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/results/<task_id>')
def get_results(task_id):
    try:
        if task_id in processing_results:
            return jsonify(processing_results[task_id])
        elif task_id in processing_status:
            status = processing_status[task_id]
            if status['status'] == 'processing':
                return jsonify({'message': 'Processing still in progress'}), 202
            elif status['status'] == 'error':
                return jsonify({'error': status['message']}), 500
            else:
                return jsonify({'error': 'Results not available'}), 404
        else:
            return jsonify({'error': 'Task not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    try:
        # Check if YOLO model can be loaded
        model = YOLO(MODEL_PATH)
        return jsonify({
            'status': 'healthy',
            'model_loaded': True,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    print("Starting Crowd Management API Server...")
    print(f"Upload folder: {UPLOAD_FOLDER}")
    print(f"Model path: {MODEL_PATH}")
    
    # Check if model exists
    if not os.path.exists(MODEL_PATH):
        print(f"Warning: Model file not found at {MODEL_PATH}")
        print("Please ensure you have the YOLO model file in the correct location")
    
    app.run(debug=True, host='0.0.0.0', port=5000)