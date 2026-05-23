SYMPTOM_MAP = {
    "healthy":              ["active", "eating well", "normal", "no symptoms"],
    "skin_disease":         ["itching", "rash", "patches", "scabs", "hair loss", "lesions", "redness"],
    "bacterial_dermatitis": ["pus", "swelling", "hot spots", "crusting", "odor", "moist"],
    "fungal_infection":     ["circular patches", "bald spots", "scaling", "ringworm", "flaking"],
    "lumpy_skin":           ["lumps", "nodules", "fever", "swelling", "nasal discharge"],
    "foot_mouth_disease":   ["limping", "blisters", "mouth sores", "drooling", "lameness"],
    "newcastle":            ["twisting neck", "paralysis", "gasping", "green droppings"],
    "coccidiosis":          ["bloody droppings", "lethargy", "hunched", "pale comb", "weight loss"],
    "salmonella":           ["diarrhea", "weakness", "drooping wings", "loss of appetite"],
}
QUESTIONS = {
    ("dog", "healthy"):              ["Is the dog active and playful?", "Is the dog eating normally?", "Any recent changes in behavior?"],
    ("dog", "skin_disease"):         ["Is the dog scratching excessively?", "Are there visible bald patches?", "Is the skin red or inflamed?"],
    ("dog", "bacterial_dermatitis"): ["Are there hot spots or moist areas?", "Is there a bad odor from the skin?", "Is the dog licking one spot repeatedly?"],
    ("dog", "fungal_infection"):     ["Are there circular bald patches?", "Is there scaling or flaking?", "Has the dog been near other animals recently?"],
    ("cow", "healthy"):              ["Is the cow eating and drinking normally?", "Is the cow moving well?", "Any recent changes in behavior?"],
    ("cow", "lumpy_skin"):           ["Are there raised lumps or nodules on skin?", "Does the animal have a fever?", "Has it been near other sick cattle?"],
    ("cow", "foot_mouth_disease"):   ["Is the animal limping or refusing to walk?", "Are there blisters on feet or mouth?", "Is the animal drooling excessively?"],
    ("chicken", "healthy"):          ["Is the chicken eating and drinking normally?", "Is the chicken active?", "Are the droppings normal?"],
    ("chicken", "newcastle"):        ["Is the bird twisting its neck?", "Are there signs of paralysis?", "Is the bird gasping for breath?"],
    ("chicken", "coccidiosis"):      ["Are there bloody droppings?", "Is the bird hunched and lethargic?", "Is the bird losing weight?"],
    ("chicken", "salmonella"):       ["Does the bird have diarrhea?", "Are the wings drooping?", "Is the bird refusing to eat?"],
}
DEFAULT_QUESTIONS = [
    "Is the animal eating and drinking normally?",
    "How long have you noticed these symptoms?",
    "Has the animal been vaccinated recently?"
]
def get_followup_questions(animal, disease):
    return QUESTIONS.get((animal, disease), DEFAULT_QUESTIONS)
def refine_prediction(top_pred, symptoms, answers):
    disease    = top_pred["disease"]
    confidence = top_pred["confidence"] / 100
    keywords   = SYMPTOM_MAP.get(disease, [])
    matches    = sum(1 for s in symptoms if any(k in s.lower() for k in keywords))
    symptom_boost = (matches / max(len(keywords), 1)) * 0.15
    yes_count     = sum(1 for v in answers.values() if str(v).lower() == "yes")
    answer_boost  = yes_count * 0.04
    final         = min(confidence + symptom_boost + answer_boost, 0.99)
    final_pct     = round(final * 100, 2)
    if final >= 0.80:
        risk   = "HIGH"
        advice = f"High likelihood of {disease.replace('_', ' ')}. Consult a veterinarian immediately."
    elif final >= 0.50:
        risk   = "MEDIUM"
        advice = f"Possible {disease.replace('_', ' ')}. Monitor closely and consult a vet if symptoms worsen."
    else:
        risk   = "LOW"
        advice = "Confidence is low. Upload a clearer image or consult a vet directly."
    return {
        "animal":     top_pred["animal"],
        "disease":    disease,
        "confidence": final_pct,
        "risk_level": risk,
        "advice":     advice
    }