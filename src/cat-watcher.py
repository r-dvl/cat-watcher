import cv2
import datetime

from Camera import Camera
from MongoDB import MongoDB


def main():
    cam = Camera('cam', 0)
    mongo = MongoDB(MONGODB_URL, DB_NAME, COLLECTION_NAME)

    ret, frame1 = cam.get_cap()
    ret, frame2 = cam.get_cap()
    counter = 0

    while cam.cap.isOpened():
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
            if cv2.contourArea(contour) < 900:
                continue

            if counter == 100:
                motion = cam.take_photo(frame1)
                mongo.post_photo(motion, datetime.datetime.now())
                counter += 1

            elif counter > 100:
                counter = 0

            else:
                counter += 1

        frame1 = frame2
        ret, frame2 = cam.get_cap()

    cam.cap.release()

if __name__ == '__main__':
    main()
