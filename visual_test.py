import tensorflow as tf
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import json, random
from pathlib import Path
preprocess = tf.keras.applications.efficientnet.preprocess_input
def test_random_images(animal, n=5):
    model = tf.keras.models.load_model(f"models/{animal}_best.keras")
    with open(f"models/{animal}_classes.json") as f:
        class_names = json.load(f)
    print(f"\n{'='*50}")
    print(f"  VISUAL TEST: {animal.upper()}")
    print(f"{'='*50}")
    test_path = Path(f"dataset/test/{animal}")
    all_images = []
    for cls_folder in test_path.iterdir():
        if cls_folder.is_dir():
            imgs = list(cls_folder.glob("*.jpg")) + list(cls_folder.glob("*.png"))
            for img in imgs:
                all_images.append((img, cls_folder.name))
    random.shuffle(all_images)
    samples = all_images[:n]
    correct = 0
    for img_path, true_label in samples:
        img = Image.open(img_path).convert("RGB").resize((224, 224))
        arr = np.array(img, dtype=np.float32)
        arr = preprocess(arr)
        arr = np.expand_dims(arr, axis=0)
        preds      = model.predict(arr, verbose=0)[0]
        pred_idx   = np.argmax(preds)
        pred_label = class_names[pred_idx]
        confidence = preds[pred_idx] * 100
        status     = "✓" if pred_label == true_label else "✗ WRONG"
        if pred_label == true_label:
            correct += 1
        print(f"  {status} | True: {true_label:25} | Predicted: {pred_label:25} | {confidence:.1f}%")
    print(f"\n  Result: {correct}/{n} correct")
test_random_images("dog",     n=10)
test_random_images("cow",     n=10)
test_random_images("chicken", n=10)