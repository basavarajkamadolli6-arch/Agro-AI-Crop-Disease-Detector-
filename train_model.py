
import tensorflow as tf
from pathlib import Path

# Dataset folder
DATA_DIR = Path(r"C:\AgroAI\dataset\raw\color")

# Model settings
IMAGE_SIZE = (128, 128)
BATCH_SIZE = 32
SEED = 42

print("TensorFlow version:", tf.__version__)
print("Loading plant disease images...")

# Load images and create training/validation datasets
train_ds = tf.keras.utils.image_dataset_from_directory(
    DATA_DIR,
    validation_split=0.2,
    subset="training",
    seed=SEED,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="int"
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    DATA_DIR,
    validation_split=0.2,
    subset="validation",
    seed=SEED,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="int"
)

class_names = train_ds.class_names

print("\nTotal classes:", len(class_names))
print("Training batches:", tf.data.experimental.cardinality(train_ds).numpy())
print("Validation batches:", tf.data.experimental.cardinality(val_ds).numpy())

# Save class names for the Django backend
Path(r"C:\AgroAI\backend").mkdir(parents=True, exist_ok=True)

with open(r"C:\AgroAI\backend\classes.txt", "w", encoding="utf-8") as file:
    file.write("\n".join(class_names))

print("\nClass names saved to C:\\AgroAI\\backend\\classes.txt")

# Improve input performance
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)

# Create a basic CNN model
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(128, 128, 3)),
    tf.keras.layers.Rescaling(1.0 / 255),
    tf.keras.layers.Conv2D(32, 3, activation="relu"),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Conv2D(64, 3, activation="relu"),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Conv2D(128, 3, activation="relu"),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(len(class_names), activation="softmax")
])

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

print("\nStarting model training...")

model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=5
)

# Save trained model
MODEL_PATH = r"C:\AgroAI\backend\plant_disease_model.keras"
model.save(MODEL_PATH)

print("\nTraining completed!")
print("Model saved to:", MODEL_PATH)
