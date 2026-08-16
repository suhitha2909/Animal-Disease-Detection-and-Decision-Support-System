# VetScan : Animal Disease Detection System

AI-assisted disease detection for dogs, cows, and chickens using
EfficientNetB0 transfer learning + Grad-CAM + symptom-guided confidence refinement.

---

## Files in this project

| File | Purpose |
|------|---------|
| `sort_data.py` | Copy raw dog/cow images into `dataset/` with correct splits |
| `sort_chicken.py` | Copy raw chicken images into `dataset/train/chicken/` |
| `remove_duplicates.py` | Remove duplicate/corrupt images using perceptual hashing |
| `split.py` | **MOVE** 15% to val and 15% to test (no leakage) |
| `train.py` | Train one model per animal, print honest test-set metrics |
| `evaluate.py` | Standalone evaluation per-class report + confusion matrix |
| `app.py` | Flask API backend |
| `animal_detector.py` | ImageNet-based gating check (is this actually the right animal?) |
| `gradcam.py` | Grad-CAM heatmap generation |
| `decision_support.py` | Follow-up questions + confidence refinement logic |
| `index.html` | Frontend UI |

---

## Run order

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Put your raw data in:
#    raw_data/raw_dog/     (see sort_data.py for expected subfolder structure)
#    raw_data/raw_cow/
#    raw_data/raw_chicken/Train/

# 3. Remove duplicate images
python remove_duplicates.py

# 4. Sort images into dataset/
python sort_data.py
python sort_chicken.py

# 5. Split into train / val / test  (uses MOVE , no data leakage)
python split.py

# 6. Train
python train.py
#    → prints per-class report on the test set at the end of each animal

# 7. (Optional) Re-evaluate any time
python evaluate.py
python evaluate.py --animal dog

# 8. Start the API
python app.py

# 9. Open index.html in a browser
```

---

## What was wrong before (and what was fixed)

### 🔴 Bug 1 : Data leakage in `split.py`  (CRITICAL)
**Old code** used `shutil.copy2()`, so images were copied to val/test but
the originals stayed in `dataset/train/`.  The model trained on the same
images it was validated on → artificially perfect 0.97 / 0.99 accuracy.

**Fix:** `split.py` now uses `shutil.move()`.  Val and test images are
physically removed from train.  There is zero overlap between splits.

### 🔴 Bug 2 : Leakage in `sort_data.py`
**Old code** mapped `raw_dog/valid/` and `raw_dog/test/` to
`dataset/train/dog/`  the dataset's original test split was being used
for training.

**Fix:** `sort_data.py` now maps:
- `raw_dog/valid/ → dataset/val/dog/`
- `raw_dog/test/  → dataset/test/dog/`

### 🟡 Bug 3 : Too little regularisation in `train.py`
Dropout was 0.3 / 0.2.  With a powerful ImageNet backbone and only
~150 images per class, this was not enough.

**Fix:**
- Dropout raised to 0.5 / 0.4
- L2 weight decay added to the Dense layer
- Phase-2 fine-tuning unfreezes only the **top 30 layers** of the backbone
  (full fine-tuning on small data = overfitting)
- Class-balanced loss weights added (handles imbalanced datasets)

### 🟡 Bug 4 : No honest evaluation
Training only reported training/val accuracy, never test accuracy.

**Fix:** `train.py` now evaluates on the held-out test set after training
and prints a per-class `classification_report` + confusion matrix.
A standalone `evaluate.py` is also provided.

### 🟡 Bug 5 : `gradcam.py` returned a flat string
**Old:** `get_gradcam()` returned a single base64 string.
**Fix:** returns `{"overlay": ..., "heatmap": ...}` so the frontend can
show both the coloured overlay and, optionally, the raw activation map.
`app.py` updated to match.

---

## Expected real-world accuracy (after fixes)

| Animal | Realistic test accuracy |
|--------|------------------------|
| Dog    | 75–85 % |
| Cow    | 78–87 % |
| Chicken| 80–88 % |

These are honest numbers.  A val accuracy of 99 % on a 150-image-per-class
dataset is always a sign of leakage, not a sign of a good model.

---

## How confidence refinement works

The disease model outputs a raw softmax probability (0–100 %).
This is shown as the initial prediction.

After the user answers follow-up questions, `decision_support.py`:
1. Matches symptom keywords → +0–10 % boost
2. Counts "yes" answers → +0–5 % boost
3. Hard cap: symptoms cannot push a weak model prediction (< 45 %) above 55 %
4. Total adjustment capped at ±15 %  symptoms never override the model

Risk bands:
- **HIGH**   ≥ 75 % → consult vet immediately
- **MEDIUM** 45–74 % → monitor and consult if worsening
- **LOW**    < 45 % → unclear, get a clearer image or direct vet consult

## Team Members

- Suhitha
- Jaswanth Kesanapalli
- Lavanya
