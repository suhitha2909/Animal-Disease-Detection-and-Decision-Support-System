import shutil
from pathlib import Path
remove_these = [
    "dataset/train/chicken/_unsorted",
    "dataset/val/chicken/_unsorted",
    "dataset/test/chicken/_unsorted",
    "dataset/train/chicken/respiratory",
    "dataset/val/chicken/respiratory",
    "dataset/test/chicken/respiratory",
    "dataset/train/cow/brd_respiratory",
    "dataset/val/cow/brd_respiratory",
    "dataset/test/cow/brd_respiratory",
]
for folder in remove_these:
    p = Path(folder)
    if p.exists():
        shutil.rmtree(p)
        print(f"Removed: {folder}")
    else:
        print(f"Already gone: {folder}")
print("\nCleanup done.")
