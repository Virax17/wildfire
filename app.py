from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os

app = Flask(__name__)
model = tf.keras.models.load_model("models/fire_smoke_model.keras")

class_names = ['fire', 'smoke', 'no_fire_smoke']
os.makedirs("uploads", exist_ok=True)

def get_geotag(image_path):
    """Extracts GPS metadata from an image (if available)."""
    image = Image.open(image_path)
    exif_data = image._getexif()
    if not exif_data:
        return None

    gps_info = {}
    for tag, value in exif_data.items():
        tag_name = TAGS.get(tag, tag)
        if tag_name == "GPSInfo":
            for key, val in value.items():
                gps_info[GPSTAGS.get(key, key)] = val

    if "GPSLatitude" in gps_info and "GPSLongitude" in gps_info:
        lat = gps_info["GPSLatitude"]
        lon = gps_info["GPSLongitude"]
        lat = lat[0] + lat[1]/60 + lat[2]/3600
        lon = lon[0] + lon[1]/60 + lon[2]/3600
        return {"lat": lat, "lon": lon}
    
    return None

def predict_image(image_path):
    """Preprocesses the image and makes a prediction."""
    img = Image.open(image_path).convert("RGB").resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

    prediction = model.predict(img_array)
    predicted_class = class_names[np.argmax(prediction)]
    confidence = np.max(prediction) * 100
    return predicted_class, confidence

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    file_path = os.path.join("uploads", file.filename)
    file.save(file_path)

    predicted_class, confidence = predict_image(file_path)
    geo_location = get_geotag(file_path)

    return jsonify({
        'prediction': predicted_class,
        'confidence': confidence,
        'location': geo_location
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

