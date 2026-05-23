import imagehash
from PIL import Image
from pathlib import Path
def remove_dupes(folder):
    folder = Path(folder)
    if not folder.exists():
        print(f"NOT FOUND: {folder}")
        return
    hashes  = {}
    removed = 0
    all_imgs = list(folder.rglob("*.jpg")) + list(folder.rglob("*.jpeg")) + list(folder.rglob("*.png"))
    for img_path in all_imgs:
        try:
            h = str(imagehash.phash(Image.open(img_path)))
            if h in hashes:
                img_path.unlink()
                removed += 1
            else:
                hashes[h] = img_path
        except:
            img_path.unlink()
            removed += 1
    print(f"{folder.name}: removed {removed} duplicates/corrupt images")
remove_dupes("raw_data/raw_dog")
remove_dupes("raw_data/raw_cow")
remove_dupes("raw_data/raw_chicken")
print("Done.")
