import cv2
from Controllers.realsense_camera import RealSenseCamera
from Controllers.face_controller import FaceController

class FaceTracker:
    def __init__(self, face_cascade_path):
        self.camera = RealSenseCamera()
        self.face = FaceController()
        self.face_cascade = cv2.CascadeClassifier(face_cascade_path)

    def detect_face(self, frame):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        return faces

    def calculate_face_center(self, face):
        x, y, w, h = face
        center_x = x + w // 2
        center_y = y + h // 2
        return center_x, center_y

    def track_face(self):
        self.face.turn_part("ON", "EYES")
        
        while True:
            color_frame = self.camera.get_color_frame()
            depth_frame = self.camera.get_depth_frame()

            if color_frame is None or depth_frame is None:
                continue

            faces = self.detect_face(color_frame)

            if len(faces) > 0:
                face = faces[0]
                center_x, center_y = self.calculate_face_center(face)

                distance = self.camera.get_distance((center_x, center_y))

                if distance is not None:
                    eyes_point = self.camera.get_eyes_point([float(center_x), float(center_y), float(distance), 1])
                    cv2.circle(color_frame, (center_x, center_y), 5, (0, 255, 0), -1)
                    text = f"x={eyes_point[0]}, y={eyes_point[1]}, d={eyes_point[2]}"
                    cv2.putText(color_frame, text, (center_x + 10, center_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

                    self.face.look_at(eyes_point)
                    
            for (x, y, w, h) in faces:
                cv2.rectangle(color_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            cv2.imshow("Face Tracker", color_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.face.close_connection()
        self.camera.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    face_tracker = FaceTracker("face_recognition/haarcascade_frontalface_alt.xml")
    face_tracker.track_face()
