import os
import cv2
import datetime
import base64
import asyncio
import aiohttp


async def post_photo(url, headers, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            print(f'Response status: {response.status}')
            return await response.text()

def main():
    # API Params
    token =  os.environ['TOKEN']
    url = os.environ['API_URL']

    # Motion Params
    counter = 0
    tolerance = 200
    sensibility = 1000
    camera_number = 0   # Any
    
    # Camera and frames init
    camera = cv2.VideoCapture(camera_number)
    ret, frame1 = camera.read()
    ret, frame2 = camera.read()

    try:
        while camera.isOpened():
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
                if cv2.contourArea(contour) < sensibility:
                    continue

                if counter == tolerance:
                    print("Movement!")

                    # Data
                    photo = base64.b64encode(cv2.imencode('.jpg', frame1)[1]).decode('utf-8')
                    date = datetime.datetime.now()

                    # HTTP Request body and header
                    data = {"date": f"{date}", "image": f"{photo}"}
                    headers = {"Authorization": f"{token}"}

                    # HTTP Request
                    asyncio.run(post_photo(f"{url}/photos/upload", headers, data))

                    counter += 1

                elif counter > tolerance:
                    counter = 0

                else:
                    counter += 1

            frame1 = frame2
            ret, frame2 = camera.read()

    except Exception as error:
        print(f"Error or interruption: {error}")

    camera.release()


if __name__ == '__main__':
    main()
