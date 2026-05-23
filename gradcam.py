import numpy as np
import tensorflow as tf
import cv2, base64
from PIL import Image
import io
def get_gradcam(model, img_array, class_idx):
    last_conv = None
    for layer in reversed(model.layers):
        if isinstance(layer, tf.keras.layers.Conv2D):
            last_conv = layer.name
            break
    if last_conv is None:
        last_conv = "top_conv"
    grad_model = tf.keras.Model(
        inputs  = model.inputs,
        outputs = [model.get_layer(last_conv).output, model.output]
    )
    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_array)
        loss = predictions[:, class_idx]
    grads   = tape.gradient(loss, conv_outputs)
    weights = tf.reduce_mean(grads, axis=(0, 1, 2))
    cam     = tf.reduce_sum(tf.multiply(weights, conv_outputs[0]), axis=-1)
    cam     = tf.maximum(cam, 0)
    cam     = cam / (tf.math.reduce_max(cam) + 1e-8)
    cam     = cam.numpy()
    cam_resized = cv2.resize(cam, (224, 224))
    cam_colored = cv2.applyColorMap(np.uint8(255 * cam_resized), cv2.COLORMAP_JET)
    orig = img_array[0].copy()
    orig[..., 0] += 103.939
    orig[..., 1] += 116.779
    orig[..., 2] += 123.68
    orig = np.clip(orig, 0, 255).astype(np.uint8)
    orig = cv2.cvtColor(orig, cv2.COLOR_RGB2BGR)
    overlay = cv2.addWeighted(orig, 0.6, cam_colored, 0.4, 0)
    _, buf  = cv2.imencode(".jpg", overlay)
    return base64.b64encode(buf).decode("utf-8")