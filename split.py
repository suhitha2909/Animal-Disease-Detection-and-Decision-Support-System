"""
split.py
========
Cuts val (15%) and test (15%) from dataset/train by MOVING files.
Uses shutil.move() — images physically leave dataset/train/.
There is zero overlap between train / val / test after this runs.
Run after: sort_data.py + sort_chicken.py
Run before: train.py
"""
import shutil
import random
from pathlib import Path
random.seed(42)
MIN_WARN = 50
for split in ["val", "test"]:
    p = Path(f"dataset/{split}")
    if p.exists():
        shutil.rmtree(p)
        print(f"Cleared dataset/{split}/")
SOURCE = Path("dataset/train")
print("\n=== COUNTS BEFORE SPLIT ===")
for animal in sorted(SOURCE.iterdir()):
    if not animal.is_dir():
        continue
    for disease in sorted(animal.iterdir()):
        if not disease.is_dir():
            continue
        imgs = (list(disease.glob("*.jpg"))
              + list(disease.glob("*.jpeg"))
              + list(disease.glob("*.png")))
        print(f"  {animal.name:10s} / {disease.name:25s}  {len(imgs):5d}")
print("\nSplitting (MOVING files — no leakage) …")
for animal in sorted(SOURCE.iterdir()):
    if not animal.is_dir():
        continue
    for disease in sorted(animal.iterdir()):
        if not disease.is_dir():
            continue
        imgs = (list(disease.glob("*.jpg"))
              + list(disease.glob("*.jpeg"))
              + list(disease.glob("*.png")))
        random.shuffle(imgs)
        n = len(imgs)
        val_imgs  = imgs[int(n * 0.70) : int(n * 0.85)]
        test_imgs = imgs[int(n * 0.85):]
        for img in val_imgs:
            dest = Path("dataset/val") / animal.name / disease.name
            dest.mkdir(parents=True, exist_ok=True)
            shutil.move(str(img), dest / img.name)
        for img in test_imgs:
            dest = Path("dataset/test") / animal.name / disease.name
            dest.mkdir(parents=True, exist_ok=True)
            shutil.move(str(img), dest / img.name)
print("\n=== FINAL SPLIT SUMMARY ===")
for split in ["train", "val", "test"]:
    p = Path(f"dataset/{split}")
    if not p.exists():
        continue
    print(f"\n  {split}/")
    for animal in sorted(p.iterdir()):
        if not animal.is_dir():
            continue
        for disease in sorted(animal.iterdir()):
            if not disease.is_dir():
                continue
            imgs = (list(disease.glob("*.jpg"))
                  + list(disease.glob("*.jpeg"))
                  + list(disease.glob("*.png")))
            warn = "  ⚠ TOO FEW" if len(imgs) < MIN_WARN else ""
            print(f"    {animal.name:10s} / {disease.name:25s}  {len(imgs):5d}{warn}")
print("\nDone — no overlap between splits.")
print("Next: python train.py")