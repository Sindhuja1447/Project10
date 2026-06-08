import cv2
import numpy as np
import time
import argparse

print("Starting Fatigue Monitor...")

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--hydration_interval', type=int, default=1800, help='Hydration reminder interval in seconds')
parser.add_argument('--fatigue_threshold', type=int, default=25, help='Fatigue threshold in blinks per minute')
parser.add_argument('--drowsiness_threshold', type=int, default=10, help='Drowsiness threshold in seconds')
args = parser.parse_args()

HYDRATION_INTERVAL = args.hydration_interval
FATIGUE_THRESHOLD = args.fatigue_threshold
DROWSINESS_THRESHOLD = args.drowsiness_threshold
print(f"Hydration interval set to {HYDRATION_INTERVAL} seconds")
print(f"Fatigue threshold set to {FATIGUE_THRESHOLD} blinks/min")
print(f"Drowsiness threshold set to {DROWSINESS_THRESHOLD} seconds")

def speak_once(text):
    import pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Unable to open the camera.")
    exit(1)

cv2.namedWindow("Fatigue Monitor", cv2.WINDOW_NORMAL)
print("Camera opened successfully")

# show first frame quickly while initializing models
ret, init_frame = cap.read()
if ret:
    cv2.putText(init_frame, "Initializing monitor...", (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
    cv2.imshow("Fatigue Monitor", init_frame)
    cv2.waitKey(1)

# ---------- MEDIAPIPE ----------
import os
import urllib.request
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

model_path = os.path.join(os.path.dirname(__file__), 'face_landmarker.task')
if not os.path.exists(model_path):
    print("Downloading Face Landmarker model...")
    url = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task"
    urllib.request.urlretrieve(url, model_path)

base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    num_faces=1,
    min_face_detection_confidence=0.5,
    min_face_presence_confidence=0.5,
    min_tracking_confidence=0.5)
detector = vision.FaceLandmarker.create_from_options(options)

LEFT_EYE = [33,160,158,133,153,144]
RIGHT_EYE = [362,385,387,263,373,380]

# ---------- VARIABLES ----------
total_blinks = 0
fatigue_blinks = 0
eye_closed = False
eye_closed_start = None
hydration_timer = time.time()
rate_start_time = time.time()
fatigue_start_time = time.time()

EAR_THRESHOLD = 0.20  # Lowered for better detection on tilted faces
EYE_OPEN_THRESHOLD = 0.25
MIN_BLINK_DURATION = 0.08
DROWSY_TIME = DROWSINESS_THRESHOLD  # seconds eyes closed (configurable)
FATIGUE_TIME = 60         # fatigue check window

alert_message = ""
alert_end_time = 0
voice_played = False

# ---------- EAR FUNCTION ----------
def eye_aspect_ratio(eye):
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    return (A + B) / (2.0 * C)

# ---------- MAIN LOOP ----------
try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Warning: Frame not read from camera.")
            continue

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        results = detector.detect(mp_image)

        if results.face_landmarks:
            mesh_points = np.array(
                [(p.x * frame.shape[1], p.y * frame.shape[0], p.z)
                 for p in results.face_landmarks[0]])

            left_eye = mesh_points[LEFT_EYE]
            right_eye = mesh_points[RIGHT_EYE]

            ear = (eye_aspect_ratio(left_eye) +
                   eye_aspect_ratio(right_eye)) / 2

            # ---------- BLINK DETECTION ----------
            if ear < EAR_THRESHOLD:
                if not eye_closed:
                    eye_closed = True
                    eye_closed_start = time.time()
            elif ear > EYE_OPEN_THRESHOLD:
                if eye_closed:
                    closed_duration = time.time() - eye_closed_start
                    if closed_duration >= MIN_BLINK_DURATION:
                        total_blinks += 1
                        fatigue_blinks += 1
                    eye_closed = False
                    eye_closed_start = None

            # ---------- SHOW EYE CLOSED TIMER ----------
            if eye_closed_start is not None:
                closed_time = int(time.time() - eye_closed_start)
                cv2.putText(frame, f"Eyes Closed: {closed_time}s",
                            (30, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                            (0,255,255), 2)

            # ---------- BLINK RATE DISPLAY ----------
            elapsed_time = max(1.0, time.time() - rate_start_time)
            blink_rate = (total_blinks / elapsed_time) * 60.0
            cv2.putText(frame, f"Blink Rate: {blink_rate:.1f}/min",
                        (30, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (0,0,0), 2)
            cv2.putText(frame, f"Blink Count: {total_blinks}",
                        (30, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (0,0,0), 2)

            # ---------- DROWSINESS DETECTION ----------
            if eye_closed_start is not None:
                closed_duration = time.time() - eye_closed_start

                if closed_duration > 0.5:  # ignore blinks
                    if closed_duration > DROWSY_TIME:
                        if time.time() > alert_end_time:
                            alert_message = "DROWSINESS DETECTED"
                            alert_end_time = time.time() + 10   # 
                            voice_played = False
                        eye_closed = False
                        eye_closed_start = None

            # ---------- FATIGUE DETECTION ----------
            if time.time() - fatigue_start_time > FATIGUE_TIME:
                if fatigue_blinks > FATIGUE_THRESHOLD:
                    if time.time() > alert_end_time:
                        alert_message = "FATIGUE DETECTED"
                        alert_end_time = time.time() + 10
                        voice_played = False
                fatigue_blinks = 0
                fatigue_start_time = time.time()

        # ---------- HYDRATION REMINDER ----------
        if time.time() - hydration_timer > HYDRATION_INTERVAL:
            if time.time() > alert_end_time:
                alert_message = "DRINK WATER"
                alert_end_time = time.time() + 10
                voice_played = False
            hydration_timer = time.time()

        # ---------- SHOW ALERT ON SCREEN ----------
        if time.time() < alert_end_time:

            # dark background for visibility
            cv2.rectangle(frame, (20,120), (620,260), (0,0,0), -1)

            # large centered alert text
            cv2.putText(frame, alert_message,
                        (40,210),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.3,
                        (0,0,255),
                        4)

            # voice alert
            if not voice_played:
                if alert_message == "DROWSINESS DETECTED":
                    speak_once("Drowsiness detected. Please freshen up or take a short walk")

                elif alert_message == "FATIGUE DETECTED":
                    speak_once("Fatigue detected. Please take a short break")

                elif alert_message == "DRINK WATER":
                    speak_once("Reminder. Please drink some water")

                voice_played = True

        cv2.imshow("Fatigue Monitor", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break
except Exception as e:
    print(f"Error in main loop: {e}")
finally:
    cap.release()
    cv2.destroyAllWindows()