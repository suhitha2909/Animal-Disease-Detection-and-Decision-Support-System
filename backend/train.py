import tensorflow as tf
from tensorflow.keras import layers, Model
from tensorflow.keras.applications import EfficientNetB0
import json, os
from pathlib import Path
IMG_SIZE   = (224, 224)
BATCH      = 16
AUTOTUNE   = tf.data.AUTOTUNE
preprocess = tf.keras.applications.efficientnet.preprocess_input
augment = tf.keras.Sequential([
    tf.keras.layers.RandomFlip("horizontal_and_vertical"),
    tf.keras.layers.RandomRotation(0.3),
    tf.keras.layers.RandomZoom(0.2),
    tf.keras.layers.RandomContrast(0.3),
    tf.keras.layers.RandomBrightness(0.2),
    tf.keras.layers.GaussianNoise(0.05),
])
def build_model(num_classes):
    inputs   = layers.Input(shape=(224, 224, 3))
    backbone = EfficientNetB0(
        include_top=False,
        weights="imagenet",
        input_tensor=inputs
    )
    backbone.trainable = False
    x = backbone.output
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.5)(x)
    x = layers.Dense(256, activation="relu",
                     kernel_regularizer=tf.keras.regularizers.l2(0.001))(x)
    x = layers.Dropout(0.4)(x)
    outputs = layers.Dense(num_classes, activation="softmax")(x)
    return Model(inputs, outputs)
def load_ds(animal, split):
    path = f"dataset/{split}/{animal}"
    if not os.path.exists(path):
        return None, None
    ds = tf.keras.utils.image_dataset_from_directory(
        path,
        image_size=IMG_SIZE,
        batch_size=BATCH,
        label_mode="int",
        shuffle=(split == "train")
    )
    class_names = ds.class_names
    ds = ds.map(lambda x, y: (preprocess(x), y), num_parallel_calls=AUTOTUNE)
    if split == "train":
        ds = ds.map(
            lambda x, y: (augment(x, training=True), y),
            num_parallel_calls=AUTOTUNE
        )
    return ds.prefetch(AUTOTUNE), class_names
os.makedirs("models", exist_ok=True)
ANIMALS = ["chicken"]
print(f"Animals found: {ANIMALS}")
for animal in ANIMALS:
    print(f"\n{'='*50}")
    print(f"  Training: {animal.upper()}")
    print(f"{'='*50}")
    train_ds, class_names = load_ds(animal, "train")
    val_ds,   _           = load_ds(animal, "val")
    if train_ds is None:
        print(f"  No data for {animal}, skipping.")
        continue
    print(f"  Classes: {class_names}")
    num_classes = len(class_names)
    with open(f"models/{animal}_classes.json", "w") as f:
        json.dump(class_names, f)
    model = build_model(num_classes)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(1e-3),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )
    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            patience=6,
            restore_best_weights=True,
            monitor="val_loss"
        ),
        tf.keras.callbacks.ModelCheckpoint(
            f"models/{animal}_best.keras",
            save_best_only=True,
            monitor="val_loss"
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            factor=0.5, patience=3,
            monitor="val_loss", verbose=1
        ),
    ]
    print(f"\n  Phase 1: Frozen backbone...")
    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=25,
        callbacks=callbacks,
        verbose=1
    )
    print(f"\n  Phase 2: Fine-tuning last 30 layers...")
    for layer in model.layers[:-30]:
        layer.trainable = False
    for layer in model.layers[-30:]:
        layer.trainable = True
    model.compile(
        optimizer=tf.keras.optimizers.Adam(5e-5),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )
    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=25,
        callbacks=callbacks,
        verbose=1
    )
    print(f"\n  {animal.upper()} model saved.")
print("\nAll models trained.")