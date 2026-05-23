import tensorflow as tf
import numpy as np
from PIL import Image
import io
ANIMAL_IMAGENET_MAP = {
    "dog": list(range(151, 269)),
    "cow": [345, 346, 347, 348, 349, 350],
    "chicken": None,
}
_detector = None
def load_detector():
    global _detector
    if _detector is None:
        print("Loading animal detector (EfficientNetB0 ImageNet)...")
        _detector = tf.keras.applications.EfficientNetB0(
            weights="imagenet", include_top=True
        )
        print("Animal detector loaded.")
    return _detector
def detect_animal(image_bytes, selected_animal=None, threshold=0.10):
    """
    Detect which animal is present in the image using ImageNet class probabilities.
    For chicken: ImageNet cannot detect droppings. If the user explicitly
    selected 'chicken', we trust that selection and return immediately.
    For dog and cow: sum ImageNet class probabilities for known breed/species
    ranges. Reject if best score is below threshold.
    Args:
        image_bytes:      raw bytes of the uploaded image
        selected_animal:  the animal the user selected in the frontend
                          ("dog", "cow", "chicken", or None for auto-detect)
        threshold:        minimum score to accept a detection (default 0.10)
    Returns:
        (animal_name, confidence_score)  or  (None, 0.0) if rejected
    """
    if selected_animal == "chicken":
        return "chicken", 1.0
    model = load_detector()
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB").resize((224, 224))
    arr = np.array(img, dtype=np.float32)
    arr = tf.keras.applications.efficientnet.preprocess_input(arr)
    arr = np.expand_dims(arr, axis=0)
    preds = model.predict(arr, verbose=0)[0]
    detectable = {
        animal: indices
        for animal, indices in ANIMAL_IMAGENET_MAP.items()
        if indices is not None
    }
    scores = {
        animal: float(sum(preds[i] for i in indices))
        for animal, indices in detectable.items()
    }
    if selected_animal in detectable:
        selected_score = scores[selected_animal]
        if selected_score < threshold:
            return None, 0.0
        return selected_animal, round(selected_score, 4)
    if not scores:
        return None, 0.0
    best       = max(scores, key=scores.get)
    best_score = scores[best]
    if best_score < threshold:
        return None, 0.0
    return best, round(best_score, 4)