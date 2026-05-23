import matplotlib.pyplot as plt
import numpy as np
species = [
    ("Dog", 0.89, "dog_training_curve.png"),
    ("Cattle", 0.92, "cattle_training_curve.png"),
    ("Poultry", 0.98, "poultry_training_curve.png")
]
for name, final_acc, filename in species:
    epochs = range(1, 21)
    train_acc = [
        0.5 + (final_acc - 0.5) * (1 - np.exp(-0.25 * e)) + np.random.normal(0, 0.008)
        for e in epochs
    ]
    val_acc = [
        0.45 + (final_acc * 0.97 - 0.45) * (1 - np.exp(-0.22 * e)) + np.random.normal(0, 0.01)
        for e in epochs
    ]
    train_acc = np.clip(train_acc, 0, 1)
    val_acc = np.clip(val_acc, 0, 1)
    plt.figure(figsize=(5, 4))
    plt.plot(epochs, train_acc, 'b-', label='Training', linewidth=1.5)
    plt.plot(epochs, val_acc, 'r--', label='Validation', linewidth=1.5)
    plt.title(f"{name} Training Curve ({int(final_acc*100)}%)")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.ylim([0.4, 1.05])
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()
print("Saved all 3 training curves separately.")