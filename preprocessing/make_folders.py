import os
animals = {
    "dog":     ["healthy", "skin_disease", "bacterial_dermatitis", "fungal_infection"],
    "cow":     ["healthy", "lumpy_skin",   "foot_mouth_disease"],
    "chicken": ["healthy", "newcastle",    "coccidiosis",          "salmonella"],
}
for split in ["train", "val", "test"]:
    for animal, diseases in animals.items():
        for disease in diseases:
            os.makedirs(f"dataset/{split}/{animal}/{disease}", exist_ok=True)
print("All folders created.")
