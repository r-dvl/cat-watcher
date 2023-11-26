import cv2


class Camera:
    # Constructor, id will define what camera is selected
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.cap = cv2.VideoCapture(self.id)

    # Returns camera capture read
    def get_cap(self):
        return self.cap.read()
