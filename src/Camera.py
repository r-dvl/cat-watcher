import cv2
import base64


class Camera:
    # Constructor, id will define what camera is selected
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.cap = cv2.VideoCapture(self.id)

    # Saves actual frame
    def take_photo(self, frame):
        return base64.b64encode(cv2.imencode('.jpg', frame)[1]).decode('utf-8')

    # Returns camera capture read
    def get_cap(self):
        return self.cap.read()
