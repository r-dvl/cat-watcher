import os
import cv2
import datetime
import base64
import asyncio

from config import api, camera
from utility import post_photo


def main():
    """
    Detects motion through a camera and takes a photo when sufficient motion is detected.
    The photos are sent to an API via an HTTP POST request.
    """
    # Camera and frames init
    cap = cv2.VideoCapture(camera.number)
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()
    
    # A cumulative amount of motion is needed to take a picture
    motion = 0

    try:
        while cap.isOpened():
            # Frame processing for motion detection
            diff = cv2.absdiff(frame1, frame2)
            diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(diff_gray, (5, 5), 0)
            _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
            dilated = cv2.dilate(thresh, None, iterations=3)
            contours, _ = cv2.findContours(
                dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            # Motion detection
            for contour in contours:

                # Sensibility threshold
                if cv2.contourArea(contour) < camera.sensibility:
                    print(f"Not enough motion: {cv2.contourArea(contour)}")
                    continue

                # Take a picture
                elif motion == camera.motion_count:
                    print("Photo!")

                    # Data
                    photo = base64.b64encode(cv2.imencode('.jpg', frame1)[1]).decode('utf-8')
                    date = datetime.datetime.now()

                    # HTTP Request body and header
                    data = {"date": f"{date}", "image": f"{photo}"}
                    headers = {"Authorization": f"{api.token}"}

                    # HTTP Request
                    asyncio.run(post_photo(f"{api.url}/photos/upload", headers, data))

                    motion += 1

                # Motion counter reset
                elif motion > camera.motion_count:
                    print("Motion reset")
                    motion = 0

                # Something is moving
                else:
                    motion += 1
                    print(f"Motion counter: {motion}")

            frame1 = frame2
            ret, frame2 = cap.read()

    except Exception as error:
        print("Error or interruption.")

    cap.release()


if __name__ == '__main__':
    main()
