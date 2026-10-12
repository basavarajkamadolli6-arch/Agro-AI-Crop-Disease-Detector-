
import numpy as np
import tensorflow as tf

from PIL import Image, UnidentifiedImageError
from rest_framework.decorators import api_view
from rest_framework.response import Response

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "plant_disease_model.keras"
CLASSES_PATH = BASE_DIR / "classes.txt"

model = tf.keras.models.load_model(MODEL_PATH)

with open(CLASSES_PATH, "r", encoding="utf-8") as f:
    class_names = [line.strip() for line in f if line.strip()]


@api_view(["POST"])
def predict_disease(request):
    uploaded_image = request.FILES.get("image")

    if uploaded_image is None:
        return Response(
            {"error": "No image received. Send the image using the field name 'image'."},
            status=400
        )

    try:
        uploaded_image.seek(0)

        with Image.open(uploaded_image) as img:
            if img.format not in ("JPEG", "PNG"):
                return Response(
                    {"error": "Please upload a JPG or PNG image."},
                    status=400
                )

            img = img.convert("RGB")
            img = img.resize((128, 128))
            image_array = np.asarray(img, dtype=np.float32)

        image_array = np.expand_dims(image_array, axis=0)

        predictions = model.predict(image_array, verbose=0)[0]
        best_index = int(np.argmax(predictions))

        return Response({
            "predicted_class": class_names[best_index],
            "score_percent": round(
                float(predictions[best_index]) * 100, 2
            ),
            "note": "Model score is not a guarantee of prediction accuracy."
        })

    except (UnidentifiedImageError, OSError) as e:
        return Response(
            {"error": f"Could not read image: {str(e)}"},
            status=400
        )

    except Exception as e:
        return Response(
            {"error": f"Prediction failed: {type(e).__name__}: {str(e)}"},
            status=500
        )
