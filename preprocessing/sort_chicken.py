"""
sort_chicken.py
===============
Sorts chicken images into dataset/train/chicken/<class>.
split.py will cut val and test afterwards.
Your raw_chicken folder contains:
    Train/          ← images named cocci_*, healt_*, ncd_*, salmo_*, pcr_*
    train_data.csv  ← ignored (we sort by filename prefix)
PCR images are skipped — they are microscopy lab images, not field photos,
and will confuse a visual classifier.
"""
import shutil
from pathlib import Path
PREFIX_MAP = {
    "cocci": "coccidiosis",
    "healt": "healthy",
    "ncd":   "newcastle",
    "salmo": "salmonella",
}
BASE = Path("dataset/train/chicken")
for folder in PREFIX_MAP.values():
    (BASE / folder).mkdir(parents=True, exist_ok=True)
moved   = 0
skipped = 0
unknown = []
search_dirs = [
    Path("raw_data/raw_chicken/Train"),
    Path("raw_data/raw_chicken"),
]
seen = set()
for source_dir in search_dirs:
    if not source_dir.exists():
        continue
    for img in (list(source_dir.glob("*.jpg"))
              + list(source_dir.glob("*.jpeg"))
              + list(source_dir.glob("*.png"))):
        if img in seen:
            continue
        seen.add(img)
        name = img.name.lower()
        if name.startswith("pcr"):
            skipped += 1
            continue
        matched = False
        for prefix, folder in PREFIX_MAP.items():
            if name.startswith(prefix):
                dest = BASE / folder / img.name
                if not dest.exists():
                    shutil.copy2(img, dest)
                moved += 1
                matched = True
                break
        if not matched:
            skipped += 1
            unknown.append(img.name)
print(f"Moved:   {moved}")
print(f"Skipped: {skipped}  (PCR + unrecognised)")
if unknown[:10]:
    print(f"Unrecognised sample names: {unknown[:10]}")
print()
print("Chicken class counts:")
for cls in sorted(BASE.iterdir()):
    imgs = list(cls.glob("*.jpg")) + list(cls.glob("*.jpeg")) + list(cls.glob("*.png"))
    flag = "  ⚠ LOW" if len(imgs) < 150 else ""
    print(f"  {cls.name:20s}  {len(imgs):5d}{flag}")
print("\nDone.  Next: python split.py")