
import tensorflow as tf
from pathlib import Path

model_path = r"C:\AgroAI\backend\plant_disease_model.keras"
classes_path = r"C:\AgroAI\backend\classes.txt"

print("Loading AgroAI model...")

model = tf.keras.models.load_model(model_path)

with open(classes_path, "r", encoding="utf-8") as f:
    classes = f.read().splitlines()

print("Model loaded successfully!")
print("Number of classes:", len(classes))
print("Model output classes:", model.output_shape[-1])

assert len(classes) == model.output_shape[-1], (
    "Class names and model outputs do not match!"
)

print("Class names and model outputs match.")
print("Next: test with a leaf image.")
