import cv2
from face_detector import FaceDetector
from gaze_detector import GazeDetector   # NEW

def main():
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)  # webcam
    video = cv2.VideoCapture("video.mp4")     # video file

    detector = FaceDetector()

    # Get frame width for gaze detection
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    gaze = GazeDetector(frame_width)

    paused = False
    no_face_counter = 0

    while True:
        # Webcam frame
        ret_cam, frame = cap.read()
        if not ret_cam:
            break

        faces = detector.detect_faces(frame)

        # 👉 NEW: Attention logic instead of just face detection
        looking = gaze.is_looking_center(faces)

        if not looking:
            no_face_counter += 1
        else:
            no_face_counter = 0
            paused = False

        # Pause after delay
        if no_face_counter > 30:
            paused = True

        # Read video frame ONLY if not paused
        if not paused:
            ret_vid, frame_video = video.read()
            if not ret_vid:
                video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

        # Draw face boxes
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)

        # 👉 UPDATED status logic
        if paused:
            status = "PAUSED (Not Looking)"
            color = (0, 0, 255)
        elif len(faces) == 0:
            status = "NO FACE"
            color = (0, 0, 255)
        else:
            status = "WATCHING"
            color = (0, 255, 0)

        cv2.putText(frame, status, (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        # Show windows
        cv2.imshow("Camera", frame)

        if 'frame_video' in locals():
            cv2.imshow("Video", frame_video)

        if cv2.waitKey(30) & 0xFF == 27:
            break

    cap.release()
    video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()