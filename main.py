import cv2
import pyautogui
import keyboard
from face_detector import FaceDetector
from gaze_detector import GazeDetector

def main():
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    detector = FaceDetector()
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    gaze = GazeDetector(frame_width)

    no_face_counter = 0
    system_paused = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        faces = detector.detect_faces(frame)
        looking = gaze.is_looking_center(faces)

        # Logic
        if not looking:
            no_face_counter += 1
        else:
            no_face_counter = 0

        # Pause trigger
        if no_face_counter > 45 and not system_paused:
            pyautogui.press("space")
            system_paused = True

        # Resume trigger
        if looking and system_paused:
            pyautogui.press("space")
            system_paused = False

        # Draw face box
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)

        # Status display
        if system_paused:
            status = "PAUSED"
            color = (0, 0, 255)
        elif len(faces) == 0:
            status = "NO FACE"
            color = (0, 0, 255)
        else:
            status = "WATCHING"
            color = (0, 255, 0)

        cv2.putText(frame, status, (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        # 👉 SINGLE WINDOW (can minimize)
        cv2.imshow("Smart Attention System (Press Q to quit)", frame)

        # Exit key
        if keyboard.is_pressed("q"):
            break

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()