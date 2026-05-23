import os, shutil, random
from pathlib import Path
from collections import Counter
import imagehash
from PIL import Image
random.seed(42)
FINAL_CLASSES = {
    "dog":     ["healthy", "skin_disease", "fungal_infection", "bacterial_dermatitis"],
    "cow":     ["healthy", "lumpy_skin", "foot_mouth_disease"],
    "chicken": ["healthy", "newcastle", "coccidiosis", "salmonella"],
}
MAPPINGS = [
    ("raw_data/raw_dog/Dogs/Healthy",                               "dog", "healthy"),
    ("raw_data/raw_dog/Dogs/Bacterial_dermatosis",                  "dog", "bacterial_dermatitis"),
    ("raw_data/raw_dog/Dogs/Fungal_infections",                     "dog", "fungal_infection"),
    ("raw_data/raw_dog/Dogs/Hypersensitivity_allergic_dermatosis",  "dog", "skin_disease"),
    ("raw_data/raw_dog/train/Healthy",                              "dog", "healthy"),
    ("raw_data/raw_dog/train/Dermatitis",                           "dog", "bacterial_dermatitis"),
    ("raw_data/raw_dog/train/Fungal_infections",                    "dog", "fungal_infection"),
    ("raw_data/raw_dog/train/demodicosis",                          "dog", "skin_disease"),
    ("raw_data/raw_dog/train/ringworm",                             "dog", "skin_disease"),
    ("raw_data/raw_dog/train/Hypersensitivity",                     "dog", "skin_disease"),
    ("raw_data/raw_dog/valid/Healthy",                              "dog", "healthy"),
    ("raw_data/raw_dog/valid/Dermatitis",                           "dog", "bacterial_dermatitis"),
    ("raw_data/raw_dog/valid/Fungal_infections",                    "dog", "fungal_infection"),
    ("raw_data/raw_dog/valid/demodicosis",                          "dog", "skin_disease"),
    ("raw_data/raw_dog/valid/ringworm",                             "dog", "skin_disease"),
    ("raw_data/raw_dog/valid/Hypersensitivity",                     "dog", "skin_disease"),
    ("raw_data/raw_dog/test/Healthy",                               "dog", "healthy"),
    ("raw_data/raw_dog/test/Dermatitis",                            "dog", "bacterial_dermatitis"),
    ("raw_data/raw_dog/test/Fungal_infections",                     "dog", "fungal_infection"),
    ("raw_data/raw_dog/test/demodicosis",                           "dog", "skin_disease"),
    ("raw_data/raw_dog/test/ringworm",                              "dog", "skin_disease"),
    ("raw_data/raw_dog/test/Hypersensitivity",                      "dog", "skin_disease"),
    ("raw_data/raw_cow/Cows datasets/healthy",                      "cow", "healthy"),
    ("raw_data/raw_cow/Cows datasets/lumpy",                        "cow", "lumpy_skin"),
    ("raw_data/raw_cow/Cows datasets/foot-and-mouth",               "cow", "foot_mouth_disease"),
    ("raw_data/raw_cow/healthycows",                                "cow", "healthy"),
    ("raw_data/raw_cow/lumpycows",                                  "cow", "lumpy_skin"),
    ("raw_data/raw_cow/Lumpy Skin Images Dataset/Lumpy Skin",       "cow", "lumpy_skin"),
    ("raw_data/raw_cow/Lumpy Skin Images Dataset/Normal Skin",      "cow", "healthy"),
    ("raw_data/raw_cow/train",                                      "cow", "healthy"),
    ("raw_data/raw_cow/valid",                                      "cow", "healthy"),
    ("raw_data/raw_cow/test",                                       "cow", "healthy"),
]
IMG_EXTS = [".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"]
def get_images(folder):
    p = Path(folder)
    if not p.exists():
        return []
    return [f for f in p.iterdir() if f.suffix in IMG_EXTS]
print("Creating folder structure...")
for split in ["train", "val", "test"]:
    for animal, classes in FINAL_CLASSES.items():
        for cls in classes:
            os.makedirs(f"dataset/{split}/{animal}/{cls}", exist_ok=True)
print("Done.\n")
print("Collecting images...")
staging = {animal: {cls: [] for cls in classes}
           for animal, classes in FINAL_CLASSES.items()}
for src, animal, cls in MAPPINGS:
    imgs = get_images(src)
    staging[animal][cls].extend(imgs)
    if imgs:
        print(f"  {src}: {len(imgs)} images → {animal}/{cls}")
print("\nProcessing chicken images by filename...")
chicken_src = Path("raw_data/raw_chicken/Train")
CHICKEN_PREFIX = {
    "cocci": "coccidiosis",
    "healt": "healthy",
    "ncd":   "newcastle",
    "salmo": "salmonella",
}
for img in chicken_src.iterdir():
    if img.suffix not in IMG_EXTS:
        continue
    name = img.name.lower()
    if name.startswith("pcr"):
        continue
    for prefix, cls in CHICKEN_PREFIX.items():
        if name.startswith(prefix):
            staging["chicken"][cls].append(img)
            break
for cls, imgs in staging["chicken"].items():
    print(f"  chicken/{cls}: {len(imgs)} images")
print("\nRemoving duplicate images...")
for animal, classes in staging.items():
    for cls, img_list in classes.items():
        seen   = {}
        unique = []
        for img_path in img_list:
            try:
                h = str(imagehash.phash(Image.open(img_path)))
                if h not in seen:
                    seen[h] = True
                    unique.append(img_path)
            except:
                pass
        removed = len(img_list) - len(unique)
        staging[animal][cls] = unique
        if removed > 0:
            print(f"  {animal}/{cls}: removed {removed} duplicates, {len(unique)} remain")
MAX_PER_CLASS = 1500
for animal in staging:
    for cls in staging[animal]:
        if len(staging[animal][cls]) > MAX_PER_CLASS:
            random.shuffle(staging[animal][cls])
            staging[animal][cls] = staging[animal][cls][:MAX_PER_CLASS]
print("\nSplitting and copying images...")
for animal, classes in staging.items():
    for cls, img_list in classes.items():
        random.shuffle(img_list)
        n         = len(img_list)
        n_train   = int(n * 0.70)
        n_val     = int(n * 0.15)
        splits    = {
            "train": img_list[:n_train],
            "val":   img_list[n_train:n_train + n_val],
            "test":  img_list[n_train + n_val:],
        }
        for split, imgs in splits.items():
            dest = Path(f"dataset/{split}/{animal}/{cls}")
            for i, img in enumerate(imgs):
                new_name = f"{animal}_{cls}_{split}_{i:04d}{img.suffix.lower()}"
                shutil.copy2(img, dest / new_name)
print("\n" + "="*55)
print("  FINAL DATASET COUNTS")
print("="*55)
all_ok = True
for split in ["train", "val", "test"]:
    print(f"\n  {split.upper()}")
    for animal in FINAL_CLASSES:
        for cls in FINAL_CLASSES[animal]:
            p    = Path(f"dataset/{split}/{animal}/{cls}")
            imgs = list(p.glob("*.jpg")) + list(p.glob("*.png"))
            status = "OK" if len(imgs) >= 100 else "⚠ LOW"
            if len(imgs) < 100 and split == "train":
                all_ok = False
            print(f"    {animal}/{cls}: {len(imgs)}  [{status}]")
print("\n" + "="*55)
if all_ok:
    print("  All classes have enough images. Ready to train.")
else:
    print("  WARNING: Some classes are low. Check above.")
print("="*55)