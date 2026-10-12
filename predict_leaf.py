
import tensorflow as tf
import numpy as np
from pathlib import Path

MODEL_PATH = r"C:\AgroAI\backend\plant_disease_model.keras"
CLASSES_PATH = r"C:\AgroAI\backend\classes.txt"
IMAGE_PATH = input("Enter the full path of a leaf image: ").strip().strip('"')

if not Path(IMAGE_PATH).is_file():
    raise FileNotFoundError("Image not found. Check the file path.")

model = tf.keras.models.load_model(MODEL_PATH)

with open(CLASSES_PATH, "r", encoding="utf-8") as f:
    classes = f.read().splitlines()

image = tf.keras.utils.load_img(
    IMAGE_PATH,
    target_size=(128, 128)
)

image_array = tf.keras.utils.img_to_array(image)
image_array = np.expand_dims(image_array, axis=0)

predictions = model.predict(image_array, verbose=0)[0]
best_index = int(np.argmax(predictions))

print("\nPredicted class:", classes[best_index])
print("Model score:", f"{predictions[best_index] * 100:.2f}%")
print("Note: This score is not a guarantee of prediction accuracy.")
