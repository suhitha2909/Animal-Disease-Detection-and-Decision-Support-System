import os
import random
import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# ─── CONFIG ───────────────────────────────────────────────────────────────────
DATASET_ROOT = "dataset"
SPLIT        = "train"
OUTPUT_DIR   = "report_samples"
os.makedirs(OUTPUT_DIR, exist_ok=True)

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

ANIMALS = {
    "chicken": {
        "classes": ["coccidiosis", "healthy", "newcastle", "salmonella"],
        "figure_label": "Poultry",
    },
    "cow": {
        "classes": ["foot_mouth_disease", "healthy", "lumpy_skin"],
        "figure_label": "Cattle",
    },
    "dog": {
        "classes": ["bacterial_dermatitis", "fungal_infection", "healthy", "skin_disease"],
        "figure_label": "Dog",
    },
}
# ──────────────────────────────────────────────────────────────────────────────

def get_random_image(folder):
    images = [
        f for f in os.listdir(folder)
        if os.path.splitext(f)[1].lower() in IMAGE_EXTENSIONS
    ]
    if not images:
        return None
    return os.path.join(folder, random.choice(images))


def format_label(cls_name):
    """Convert folder name to a readable title."""
    return cls_name.replace("_", " ").title()


def make_grid(animal, config):
    classes     = config["classes"]
    fig_label   = config["figure_label"]
    n           = len(classes)

    # Auto grid: prefer wide layout (cols >= rows)
    cols = math.ceil(math.sqrt(n))
    rows = math.ceil(n / cols)

    fig, axes = plt.subplots(rows, cols, figsize=(cols * 4, rows * 4))
    fig.suptitle(
        f"Sample Disease Images — {fig_label}",
        fontsize=16, fontweight="bold", y=1.01
    )

    # Flatten axes for easy indexing
    if rows == 1 and cols == 1:
        axes = [[axes]]
    elif rows == 1:
        axes = [axes]
    elif cols == 1:
        axes = [[ax] for ax in axes]

    flat_axes = [axes[r][c] for r in range(rows) for c in range(cols)]

    for i, ax in enumerate(flat_axes):
        if i < n:
            cls   = classes[i]
            folder = os.path.join(DATASET_ROOT, SPLIT, animal, cls)

            if not os.path.exists(folder):
                ax.set_visible(False)
                continue

            img_path = get_random_image(folder)

            if img_path:
                img = mpimg.imread(img_path)
                ax.imshow(img)
                ax.set_title(format_label(cls), fontsize=13, fontweight="bold", pad=8)
            else:
                ax.text(0.5, 0.5, "No image found", ha="center", va="center",
                        fontsize=10, color="gray")
                ax.set_title(format_label(cls), fontsize=13, fontweight="bold", pad=8)

            ax.axis("off")
        else:
            ax.set_visible(False)  # hide unused subplots

    plt.tight_layout()

    out_path = os.path.join(OUTPUT_DIR, f"{animal}_samples.png")
    plt.savefig(out_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"  ✔ Saved: {out_path}")


def main():
    print(f"\n{'='*50}")
    print("  Generating combined sample images for report")
    print(f"{'='*50}\n")

    for animal, config in ANIMALS.items():
        print(f"  Processing: {animal.upper()} ({config['figure_label']})")
        make_grid(animal, config)

    print(f"\nAll done! Images saved in: {os.path.abspath(OUTPUT_DIR)}/\n")


if __name__ == "__main__":
    main()