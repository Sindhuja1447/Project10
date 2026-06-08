# Smart Study Break System

## Overview
Smart Study Break System is a Flask-based web application that monitors user fatigue and drowsiness using a webcam and MediaPipe Face Landmarker.

## Features
- User login and session management
- Webcam-based fatigue monitoring
- Drowsiness detection
- Blink-rate based fatigue analysis
- Hydration reminders
- Configurable thresholds
- Voice alerts using pyttsx3

## Project Structure
- app.py : Flask web application
- fatigue_monitor.py : Real-time monitoring module
- templates/ : HTML pages
- face_landmarker.task : MediaPipe model

## Requirements
- Python 3.10+
- Flask
- OpenCV
- MediaPipe
- NumPy
- pyttsx3

## Installation
```bash
pip install flask opencv-python mediapipe numpy pyttsx3
```

## Run
```bash
python app.py
```

Open:
http://127.0.0.1:5000

## Login
Username: Any non-empty username
Password: password

## Notes
The application requires a working webcam for fatigue and drowsiness detection.
