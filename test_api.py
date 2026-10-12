
import requests

url = "http://127.0.0.1:8000/api/predict/"

image_path = input("Enter the full path of a leaf image: ").strip().strip('"')

try:
    with open(image_path, "rb") as image:
        response = requests.post(
            url,
            files={"image": (image_path.split("\\")[-1], image)}
        )

    print("HTTP status:", response.status_code)
    print("API response:", response.text)

except FileNotFoundError:
    print("Error: Image file not found. Check the path.")
except requests.RequestException as error:
    print("Request error:", error)
