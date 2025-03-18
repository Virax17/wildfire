from flask import Flask, request, jsonify
from google.cloud import aiplatform
import base64
from PIL import Image
import io

app = Flask(__name__)

# ✅ Initialize Vertex AI
PROJECT_ID = "wildfire-454109"
LOCATION = "us-central1"
ENDPOINT_ID = "projects/533769998849/locations/us-central1/endpoints/3993502098384748544"

aiplatform.init(project=PROJECT_ID, location=LOCATION)
endpoint = aiplatform.Endpoint(ENDPOINT_ID)

@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    # Read and convert image to Base64
    image_file = request.files["image"]
    image = Image.open(image_file)
    img_byte_array = io.BytesIO()
    image.save(img_byte_array, format="JPEG")
    encoded_image = base64.b64encode(img_byte_array.getvalue()).decode("utf-8")

    # Send image to Vertex AI
    instances = [{"image": {"b64": encoded_image}}]
    response = endpoint.predict(instances=instances)

    return jsonify({"prediction": response.predictions})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
