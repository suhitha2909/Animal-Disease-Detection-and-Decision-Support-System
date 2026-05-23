from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import json
import os
from gradcam import get_gradcam
from decision_support import get_followup_questions, refine_prediction
from animal_detector import detect_animal
app = Flask(__name__)
CORS(app)
models = {}
classes = {}
for animal in ["dog", "cow", "chicken"]:
    model_path = f"models/{animal}_best.keras"
    class_path = f"models/{animal}_classes.json"
    if os.path.exists(model_path) and os.path.exists(class_path):
        models[animal] = tf.keras.models.load_model(model_path)
        with open(class_path, "r") as f:
            classes[animal] = json.load(f)
        print(f"Loaded {animal} model successfully")
    else:
        print(f"WARNING: Missing model or class file for {animal}")
preprocess = tf.keras.applications.efficientnet.preprocess_input
def preprocess_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    image = image.convert("RGB")
    image = image.resize((224, 224))
    image_array = np.array(image, dtype=np.float32)
    image_array = preprocess(image_array)
    image_array = np.expand_dims(image_array, axis=0)
    return image_array
@app.route("/animals", methods=["GET"])
def get_animals():
    return jsonify({
        "animals": list(models.keys()),
        "classes": classes
    })
@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({
            "error": "No image uploaded"
        }), 400
    image_bytes = request.files["image"].read()
    selected_animal = request.form.get("animal", "").lower().strip()
    symptoms = request.form.getlist("symptoms")
    detected_animal, detection_score = detect_animal(image_bytes, selected_animal=selected_animal)
    if detected_animal is None:
        return jsonify({
            "error": "invalid_image",
            "message": "Please upload a valid image of a dog, cow, or chicken."
        }), 400
    if selected_animal and detected_animal != selected_animal:
        return jsonify({
            "error": "wrong_animal",
            "message": f"You selected '{selected_animal}' but uploaded a '{detected_animal}' image."
        }), 400
    animal = selected_animal if selected_animal else detected_animal
    if animal not in models:
        return jsonify({
            "error": f"Model for '{animal}' is not available."
        }), 400
    model = models[animal]
    class_names = classes[animal]
    image_array = preprocess_image(image_bytes)
    predictions = model.predict(image_array, verbose=0)[0]
    top3_indices = np.argsort(predictions)[::-1][:3]
    top3_predictions = []
    for idx in top3_indices:
        top3_predictions.append({
            "animal": animal,
            "disease": class_names[idx],
            "confidence": round(float(predictions[idx]) * 100, 2)
        })
    heatmap = get_gradcam(
        model,
        image_array,
        int(top3_indices[0])
    )
    followup_questions = get_followup_questions(
        animal,
        class_names[top3_indices[0]]
    )
    return jsonify({
        "detected_animal": animal,
        "detection_score": detection_score,
        "predictions": top3_predictions,
        "heatmap": heatmap,
        "followup_questions": followup_questions
    })
@app.route("/refine", methods=["POST"])
def refine():
    data = request.json
    if not data or "top_prediction" not in data:
        return jsonify({
            "error": "Missing required prediction data"
        }), 400
    refined_result = refine_prediction(
        data["top_prediction"],
        data.get("symptoms", []),
        data.get("answers", {})
    )
    return jsonify(refined_result)
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "running",
        "models_loaded": list(models.keys())
    })
if __name__ == "__main__":
    app.run(debug=True, port=5000)