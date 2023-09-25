import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

# Load Data
def load_data(folder, label):
    images = []
    labels = []

    for archive in os.listdir(folder):
        if archive.endswith('.jpg'):
            image = cv2.imread(os.path.join(folder, archive))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = cv2.resize(image, (256, 256))
            image = image / 255.0  # Normalizar los píxeles

            images.append(image)
            labels.append(label)

    return np.array(images), np.array(labels)  # Devolver también las etiquetas

cats, cats_labels = load_data('./resources/cats', 1)
not_cats, not_cats_labels = load_data('./resources/not_cats', 0)

# Divide Data
X = np.concatenate((cats, not_cats), axis=0)
y = np.concatenate((cats_labels, not_cats_labels), axis=0)

X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.2, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

# Build Model
model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(256, 256, 3)),
    MaxPooling2D(pool_size=(2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train Model
history = model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=10, batch_size=32)

# Evaluate Model
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f'Test precision: {test_accuracy}')

# Save Model
model.save('cat_identifyer.keras')