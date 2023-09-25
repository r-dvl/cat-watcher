import cv2
import datetime
import base64
import numpy as np

from Camera import Camera
from MongoDB import MongoDB

from tensorflow.keras.models import load_model

model = load_model('./model/cat_identifyer.keras')

def cat_identifyier(image):
    # Image Preprocessing
    image_bytes = base64.b64decode(image)
    image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), -1)
    if image.shape[-1] == 1:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

    image = cv2.resize(image, (256, 256))
    image = image / 255.0
    image = np.expand_dims(image, axis=0)
    
    # Model Prediction
    prediction = model.predict(image)

    if prediction > 0.5:
        print("Cat!")
        return True
    else:
        print("Not a cat")
        return False

def main():
    cam = Camera('cam', 0)
    mongo = MongoDB()

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
                photo = base64.b64encode(cv2.imencode('.jpg', frame1)[1]).decode('utf-8')

                if cat_identifyier(photo):
                    mongo.post_photo(photo, datetime.datetime.now())

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
