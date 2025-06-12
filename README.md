# 🎯 Crowd Management System

A real-time CCTV video analysis system for crowd density monitoring and object detection using YOLOv8 and computer vision. This system helps security personnel and event managers monitor crowd safety and detect potential risks in real-time.

## ✨ Features

### 🔍 AI-Powered Analysis
- **Real-time Crowd Detection**: Accurate people counting using YOLOv8
- **Density Monitoring**: Calculate crowd density percentages and safety levels
- **Object Detection**: Identify vehicles, bags, and suspicious objects
- **Safety Alerts**: Automatic risk level assessment (Safe/Medium Risk/High Risk)

### 📊 Interactive Dashboard
- **Modern Web Interface**: Clean, responsive design with glassmorphism effects
- **Real-time Processing**: Live progress tracking and status updates
- **Visual Analytics**: Progress bars, statistics, and color-coded safety indicators
- **Video Upload**: Drag-and-drop file upload with format validation

### 🔐 User Management
- **Authentication System**: Secure login and signup functionality
- **Session Management**: Persistent user sessions with localStorage
- **Multi-user Support**: Individual user dashboards and data isolation

### 🛠️ Technical Features
- **Flask REST API**: Robust backend with comprehensive error handling
- **Asynchronous Processing**: Background video analysis with task queuing
- **CORS Support**: Cross-origin resource sharing for web integration
- **Health Monitoring**: API status checks and system diagnostics

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Node.js (for development)
- 4GB+ RAM (recommended for video processing)
- Webcam or CCTV video files for testing

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/lasya-14/project.git
   cd crowd-management-system
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install flask flask-cors ultralytics opencv-python numpy
   ```

4. **Create required directories**
   ```bash
   mkdir uploads results models
   ```

5. **Start the Flask server**
   ```bash
   python app.py
   ```

6. **Open the web interface**
   - Open `index.html` in your browser, or
   - Serve it using a local server:
   ```bash
   python -m http.server 8000
   ```
   Then visit `http://localhost:8000`

## 📁 Project Structure

```
crowd-management-system/
├── app.py                 # Flask backend server
├── index.html            # Frontend web interface
├── uploads/              # Uploaded video files
├── results/              # Analysis results storage
├── models/               # YOLO model files
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
```

## 🔧 Configuration

### Backend Configuration (app.py)
```python
# Server settings
UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'
MODEL_PATH = 'models/yolov8n.pt'

# Supported video formats
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm'}

# Crowd detection threshold
CROWD_THRESHOLD = 20  # people count for alerts
```

### Frontend Configuration (index.html)
```javascript
// API endpoint
const API_BASE_URL = 'http://localhost:5000';

// File size limit
const MAX_FILE_SIZE = 100 * 1024 * 1024; // 100MB
```

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API status and welcome message |
| POST | `/upload` | Upload video file for analysis |
| GET | `/status/<task_id>` | Check processing status |
| GET | `/results/<task_id>` | Retrieve analysis results |
| GET | `/health` | System health check |
| POST | `/cleanup` | Clean up old files and tasks |

### Example API Usage

```bash
# Upload video
curl -X POST -F "video=@test_video.mp4" http://localhost:5000/upload

# Check status
curl http://localhost:5000/status/task_20241215_abc123

# Get results
curl http://localhost:5000/results/task_20241215_abc123
```

## 📈 Analysis Results Format

```json
{
  "total_people": 45,
  "avg_people": 32.5,
  "max_people": 67,
  "crowd_density": 75,
  "safety_level": "Medium Risk",
  "confidence": 87,
  "vehicle_count": 3,
  "bag_count": 12,
  "suspicious_objects": 0,
  "alert_frames": 145,
  "total_frames": 1800,
  "video_duration": 60.0,
  "processed_at": "2024-12-15T10:30:00"
}
```

## 🎨 Features Showcase

### Dashboard Screenshots
- **Login Interface**: Modern glassmorphism design with gradient backgrounds
- **Upload Section**: Drag-and-drop video upload with real-time validation
- **Processing Monitor**: Live progress tracking with detailed status updates
- **Results Display**: Comprehensive analytics with color-coded safety indicators

### Safety Level Indicators
- 🟢 **Safe**: Crowd density < 50%, normal conditions
- 🟡 **Medium Risk**: Crowd density 50-70%, monitor closely
- 🔴 **High Risk**: Crowd density > 70%, immediate attention required

## 🛡️ Security Features

- **Input Validation**: File type and size validation
- **Error Handling**: Comprehensive error catching and user feedback
- **Session Management**: Secure user authentication
- **CORS Protection**: Controlled cross-origin requests

## 🔄 Development

### Adding New Features

1. **Backend (Flask)**:
   - Add new routes in `app.py`
   - Implement analysis functions
   - Update API documentation

2. **Frontend (HTML/JS)**:
   - Modify `index.html`
   - Add new UI components
   - Update JavaScript handlers

### Testing

```bash
# Test with sample video
curl -X POST -F "video=@sample_crowd_video.mp4" http://localhost:5000/upload

# Check API health
curl http://localhost:5000/health
```

## 📋 Requirements

```
flask>=2.3.0
flask-cors>=4.0.0
ultralytics>=8.0.0
opencv-python>=4.8.0
numpy>=1.24.0
```

## 🐛 Troubleshooting

### Common Issues

1. **YOLO Model Download Fails**
   ```bash
   # Manually download YOLOv8 model
   python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
   ```

2. **Video Upload Fails**
   - Check file format (mp4, avi, mov, mkv, webm)
   - Ensure file size < 100MB
   - Verify Flask server is running

3. **API Connection Issues**
   - Confirm Flask server is running on port 5000
   - Check CORS configuration
   - Verify network connectivity

### Performance Optimization

- **Large Videos**: Process every nth frame for faster analysis
- **Memory Usage**: Implement cleanup for old tasks and files
- **GPU Acceleration**: Use CUDA-enabled PyTorch for faster processing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics) for object detection
- [OpenCV](https://opencv.org/) for computer vision capabilities
- [Flask](https://flask.palletsprojects.com/) for the web framework
- Modern web design inspiration from contemporary UI/UX trends

## 📞 Support

For support, email lasyavallichavvakula@gmail.com or create an issue in the GitHub repository.

---

**Made with ❤️ for safer crowd management**
