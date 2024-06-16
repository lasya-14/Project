import cv2
import tkinter as tk 
from tkinter import filedialog

# Creating a tkinter window
root = tk.Tk()   
root.withdraw()  # Hiding the root window

# Asking the user to select a video
video_path = filedialog.askopenfilename(title="Select Video File", filetypes=[("Video Files", ".mp4;.avi;*.mkv")])

# Checking whether the video is selected or not
if not video_path:
    print("No file selected. Exiting.")  
    exit()

# Loading hogdescriptor model 
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Loading the video file
cap = cv2.VideoCapture(video_path)

# giving the crowd size
crowd_threshold = 26  

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (1000, 1000))
    #detecting the people
    (rects, _) = hog.detectMultiScale(frame, winStride=(4, 4), padding=(8, 8), scale=1.05)

    # Drawing rectangles around the people
    for (x, y, w, h) in rects:
        color = (0, 255, 0)  # green default color

        # Checking the crowd size
        if len(rects) > crowd_threshold:
            color = (0, 0, 255)  # Change color to red if crowd size exceeds the giving condition

        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

    # Display the number of people on the screen
    cv2.putText(frame, f'People: {len(rects)}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Check crowd size
    if len(rects) > crowd_threshold:
        # Highlight areas with a large crowd using a different color
        cv2.putText(frame, "Large Crowd Detected!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    else:
         cv2.putText(frame, "Normal Crowd", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255,0), 2)
    # Display the frame
    cv2.imshow('Crowd Detection', frame)

    # Breaking the condition by clicking "q"
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()