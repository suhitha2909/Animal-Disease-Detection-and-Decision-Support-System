import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report
import json, os
from pathlib import Path
IMG_SIZE   = (224, 224)
preprocess = tf.keras.applications.efficientnet.preprocess_input
ANIMALS = ["chicken","cow","dog"]
for animal in ANIMALS:
    model_path = f"models/{animal}_best.keras"
    if not os.path.exists(model_path):
        print(f"No model for {animal}, skipping.")
        continue
    print(f"\n{'='*50}")
    print(f"  Evaluating: {animal.upper()}")
    print(f"{'='*50}")
    model = tf.keras.models.load_model(model_path)
    test_ds = tf.keras.utils.image_dataset_from_directory(
        f"dataset/test/{animal}",
        image_size=IMG_SIZE,
        batch_size=32,
        label_mode="int",
        shuffle=False
    )
    class_names = test_ds.class_names
    test_ds_p   = test_ds.map(lambda x, y: (preprocess(x), y))
    all_true, all_pred = [], []
    for images, labels in test_ds_p:
        preds = model.predict(images, verbose=0)
        all_true.extend(labels.numpy())
        all_pred.extend(np.argmax(preds, axis=1))
    print(classification_report(all_true, all_pred, target_names=class_names))
    cm   = confusion_matrix(all_true, all_pred)
    disp = ConfusionMatrixDisplay(cm, display_labels=class_names)
    fig, ax = plt.subplots(figsize=(8, 6))
    disp.plot(ax=ax, xticks_rotation=45)
    plt.title(f"{animal.capitalize()} — Confusion Matrix")
    plt.tight_layout()
    plt.savefig(f"models/{animal}_confusion_matrix.png")
    print(f"Saved: models/{animal}_confusion_matrix.png")
print("\nEvaluation complete.")