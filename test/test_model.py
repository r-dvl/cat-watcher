import cv2
import numpy as np
from tensorflow.keras.models import load_model

model = load_model('./model/cats_model.keras')

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (64, 64))  # Redimensionar según el modelo
    image = image / 255.0  # Normalizar píxeles
    return np.expand_dims(image, axis=0)  # Agregar dimensión de lote

image_path = './resources/test_images/test4.jpeg'
preprocessed_image = preprocess_image(image_path)
prediction = model.predict(preprocessed_image)

if prediction > 0.5:
    print("Es un gato")
else:
    print("No es un gato")