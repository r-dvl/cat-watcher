import os
import cv2
import datetime
import base64
import asyncio

from config import api, camera
from utility import post_photo


def main():
    # Camera and frames init
    cap = cv2.VideoCapture(camera.number)
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()
    
    counter = 0

    try:
        while cap.isOpened():
            diff = cv2.absdiff(frame1, frame2)
            diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(diff_gray, (5, 5), 0)
            _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
            dilated = cv2.dilate(thresh, None, iterations=3)
            contours, _ = cv2.findContours(
                dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                (x, y, w, h) = cv2.boundingRect(contour)

                # Sensibility
                if cv2.contourArea(contour) < camera.sensibility:
                    continue

                if counter == camera.tolerance:
                    print("Movement!")

                    # Data
                    photo = base64.b64encode(cv2.imencode('.jpg', frame1)[1]).decode('utf-8')
                    date = datetime.datetime.now()

                    # HTTP Request body and header
                    data = {"date": f"{date}", "image": f"{photo}"}
                    headers = {"Authorization": f"{api.token}"}

                    # HTTP Request
                    asyncio.run(post_photo(f"{api.url}/photos/upload", headers, data))

                    counter += 1

                elif counter > camera.tolerance:
                    counter = 0

                else:
                    counter += 1

            frame1 = frame2
            ret, frame2 = cap.read()

    except Exception as error:
        print(f"Error or interruption: {error}")

    cap.release()


if __name__ == '__main__':
    main()
