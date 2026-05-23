"""
sort_data.py
============
Sorts DOG and COW images into dataset/train/ only.
split.py will cut val and test afterwards by MOVING files out.
Written for the exact folder structure visible in the project:
raw_dog/
    Dogs/
        Bacterial_dermatosis/
        Fungal_infections/
        Healthy/
        Hypersensitivity_allergic_dermatosis/
    train/ | valid/ | test/
        demodicosis/ | Dermatitis/ | Fungal_infections/
        Healthy/ | Hypersensitivity/ | ringworm/
raw_cow/
    Cows datasets/   → healthy/ | lumpy/ | foot-and-mouth/
    healthycows/
    lumpycows/
    Lumpy Skin Images Dataset/ → Lumpy Skin/ | Normal Skin/
    train/ | valid/ | test/    (Roboflow export, labelled as healthy)
Disease classes
---------------
dog  : healthy | bacterial_dermatitis | fungal_infection | skin_disease
cow  : healthy | lumpy_skin | foot_mouth_disease
"""
import shutil
from pathlib import Path
def copy_images(src, dst, tag=""):
    src_path = Path(src)
    dst_path = Path(dst)
    if not src_path.exists():
        return 0
    dst_path.mkdir(parents=True, exist_ok=True)
    count = 0
    for ext in ["*.jpg", "*.jpeg", "*.png", "*.JPG", "*.JPEG", "*.PNG"]:
        for img in src_path.glob(ext):
            prefix   = f"{tag}_" if tag else f"{src_path.name}_"
            new_name = prefix + img.name
            dest     = dst_path / new_name
            if not dest.exists():
                shutil.copy2(img, dest)
                count += 1
    if count:
        print(f"  {count:4d}  {src_path}  →  {dst_path}")
    return count
print("=" * 60)
print("DOG")
print("=" * 60)
copy_images("raw_data/raw_dog/Dogs/Healthy",                              "dataset/train/dog/healthy",               "dogs_flat")
copy_images("raw_data/raw_dog/Dogs/Bacterial_dermatosis",                 "dataset/train/dog/bacterial_dermatitis",  "dogs_flat")
copy_images("raw_data/raw_dog/Dogs/Fungal_infections",                    "dataset/train/dog/fungal_infection",      "dogs_flat")
copy_images("raw_data/raw_dog/Dogs/Hypersensitivity_allergic_dermatosis", "dataset/train/dog/skin_disease",          "dogs_flat")
for split_tag, split_dir in [("dog_tr","train"), ("dog_va","valid"), ("dog_te","test")]:
    copy_images(f"raw_data/raw_dog/{split_dir}/Healthy",           "dataset/train/dog/healthy",               split_tag)
    copy_images(f"raw_data/raw_dog/{split_dir}/Dermatitis",        "dataset/train/dog/bacterial_dermatitis",  split_tag)
    copy_images(f"raw_data/raw_dog/{split_dir}/Fungal_infections", "dataset/train/dog/fungal_infection",      split_tag)
    copy_images(f"raw_data/raw_dog/{split_dir}/demodicosis",       "dataset/train/dog/skin_disease",          split_tag)
    copy_images(f"raw_data/raw_dog/{split_dir}/ringworm",          "dataset/train/dog/skin_disease",          split_tag)
    copy_images(f"raw_data/raw_dog/{split_dir}/Hypersensitivity",  "dataset/train/dog/skin_disease",          split_tag)
print()
print("=" * 60)
print("COW")
print("=" * 60)
copy_images("raw_data/raw_cow/Cows datasets/healthy",                  "dataset/train/cow/healthy",           "cow_cd")
copy_images("raw_data/raw_cow/Cows datasets/lumpy",                    "dataset/train/cow/lumpy_skin",        "cow_cd")
copy_images("raw_data/raw_cow/Cows datasets/foot-and-mouth",           "dataset/train/cow/foot_mouth_disease","cow_cd")
copy_images("raw_data/raw_cow/healthycows",                            "dataset/train/cow/healthy",           "cow_hc")
copy_images("raw_data/raw_cow/lumpycows",                              "dataset/train/cow/lumpy_skin",        "cow_lc")
copy_images("raw_data/raw_cow/Lumpy Skin Images Dataset/Lumpy Skin",   "dataset/train/cow/lumpy_skin",        "cow_ls")
copy_images("raw_data/raw_cow/Lumpy Skin Images Dataset/Normal Skin",  "dataset/train/cow/healthy",           "cow_ls")
copy_images("raw_data/raw_cow/train", "dataset/train/cow/healthy", "cow_rf")
copy_images("raw_data/raw_cow/valid", "dataset/train/cow/healthy", "cow_rf")
copy_images("raw_data/raw_cow/test",  "dataset/train/cow/healthy", "cow_rf")
print()
print("=" * 60)
print("FINAL COUNTS  (before val/test split)")
print("=" * 60)
for animal in ["dog", "cow"]:
    p = Path(f"dataset/train/{animal}")
    if not p.exists():
        continue
    for disease in sorted(p.iterdir()):
        imgs = list(disease.rglob("*.jpg")) + list(disease.rglob("*.jpeg")) + list(disease.rglob("*.png"))
        flag = "  ⚠ LOW — need more data" if len(imgs) < 150 else ""
        print(f"  {animal:8s} / {disease.name:25s}  {len(imgs):5d}{flag}")
print("\nDone.  Next: python sort_chicken.py")