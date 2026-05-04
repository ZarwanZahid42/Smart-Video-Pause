import cv2

class GazeDetector:
    def __init__(self, frame_width):
        self.frame_width = frame_width

    def is_looking_center(self, faces):
        if len(faces) == 0:
            return False

        (x, y, w, h) = faces[0]

        face_center_x = x + w // 2

        # Define center zone (middle 40% of screen)
        left_bound = int(self.frame_width * 0.3)
        right_bound = int(self.frame_width * 0.7)

        if left_bound < face_center_x < right_bound:
            return True
        else:
            return False