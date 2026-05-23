from pathlib import Path
for cls in ["coccidiosis", "healthy", "newcastle", "salmonella"]:
    p = Path(f"dataset/test/chicken/{cls}")
    imgs = list(p.glob("*.jpg")) + list(p.glob("*.png"))
    print(f"{cls}: {len(imgs)} images")
    print(f"  First 3: {[i.name for i in imgs[:3]]}")