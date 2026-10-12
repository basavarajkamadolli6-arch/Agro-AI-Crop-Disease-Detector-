import json
import os
import tensorflow as tf

from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2


# -----------------------------
# PROJECT CONFIGURATION
# -----------------------------

PROJECT_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATASET_DIR = os.path.join(
    PROJECT_DIR,
    "dataset"
)

MODEL_DIR = os.path.join(
    PROJECT_DIR,
    "ml"
)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "disease_model.keras"
)

CLASS_NAMES_PATH = os.path.join(
    MODEL_DIR,
    "class_names.json"
)

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
SEED = 42
EPOCHS = 10


# -----------------------------
# CHECK DATASET
# -----------------------------

if not os.path.isdir(DATASET_DIR):
    raise FileNotFoundError(
        f"Dataset folder not found: {DATASET_DIR}"
    )

os.makedirs(MODEL_DIR, exist_ok=True)


# -----------------------------
# LOAD TRAINING DATA
# -----------------------------

train_dataset = tf.keras.utils.image_dataset_from_directory(
    DATASET_DIR,
    validation_split=0.2,
    subset="training",
    seed=SEED,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="int"
)

validation_dataset = tf.keras.utils.image_dataset_from_directory(
    DATASET_DIR,
    validation_split=0.2,
    subset="validation",
    seed=SEED,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="int"
)


# -----------------------------
# SAVE CLASS NAMES
# -----------------------------

class_names = train_dataset.class_names

print("\nClasses found:")

for index, name in enumerate(class_names):
    print(index, ":", name)

if len(class_names) < 2:
    raise ValueError(
        "At least two class folders are required."
    )

with open(
    CLASS_NAMES_PATH,
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        class_names,
        file,
        indent=4
    )


# -----------------------------
# IMPROVE INPUT PERFORMANCE
# -----------------------------

AUTOTUNE = tf.data.AUTOTUNE

train_dataset = train_dataset.prefetch(
    buffer_size=AUTOTUNE
)

validation_dataset = validation_dataset.prefetch(
    buffer_size=AUTOTUNE
)


# -----------------------------
# DATA AUGMENTATION
# -----------------------------

data_augmentation = models.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
])


# -----------------------------
# LOAD PRETRAINED MOBILENETV2
# -----------------------------

base_model = MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights="imagenet"
)

# Initially freeze the pretrained layers.
base_model.trainable = False


# -----------------------------
# BUILD CLASSIFICATION MODEL
# -----------------------------

inputs = layers.Input(
    shape=(224, 224, 3)
)

x = data_augmentation(inputs)

# MobileNetV2 expects pixels scaled to [-1, 1].
x = layers.Rescaling(
    scale=1.0 / 127.5,
    offset=-1
)(x)

x = base_model(
    x,
    training=False
)

x = layers.GlobalAveragePooling2D()(x)

x = layers.Dropout(0.2)(x)

outputs = layers.Dense(
    len(class_names),
    activation="softmax"
)(x)

model = models.Model(
    inputs,
    outputs
)


# -----------------------------
# COMPILE MODEL
# -----------------------------

model.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=0.001
    ),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)


# -----------------------------
# TRAIN MODEL
# -----------------------------

callbacks = [
    tf.keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=3,
        restore_best_weights=True
    )
]

history = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=EPOCHS,
    callbacks=callbacks
)


# -----------------------------
# SAVE MODEL
# -----------------------------

model.save(MODEL_PATH)

print("\nTraining completed.")

print("Model saved to:", MODEL_PATH)

print(
    "Class names saved to:",
    CLASS_NAMES_PATH
)

print(
    "Final training accuracy:",
    history.history["accuracy"][-1]
)

print(
    "Final validation accuracy:",
    history.history["val_accuracy"][-1]
)