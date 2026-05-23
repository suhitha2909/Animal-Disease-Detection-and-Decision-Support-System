import { useState, useRef } from "react";
import axios from "axios";

const SYMPTOMS = {
  dog:     ["Itching / scratching", "Hair loss", "Skin redness", "Bald patches", "Crusty skin", "Bad odor", "Hot spots", "Lethargy", "Loss of appetite"],
  cow:     ["Skin lumps / nodules", "Limping", "Mouth sores", "Drooling", "Nasal discharge", "Fever", "Loss of appetite", "Swelling"],
  chicken: ["Bloody droppings", "Drooping wings", "Twisted neck", "Gasping", "Pale comb", "Weight loss", "Diarrhea", "Lethargy"],
};

export default function Diagnose({ onResults }) {
  const [animal,   setAnimal]   = useState("");
  const [image,    setImage]    = useState(null);
  const [preview,  setPreview]  = useState(null);
  const [symptoms, setSymptoms] = useState([]);
  const [loading,  setLoading]  = useState(false);
  const [error,    setError]    = useState("");
  const fileRef = useRef();

  function handleAnimal(a) {
    setAnimal(a);
    setSymptoms([]);
    setError("");
  }

  function handleImage(e) {
    const file = e.target.files[0];
    if (!file) return;
    setImage(file);
    setPreview(URL.createObjectURL(file));
    setError("");
  }

  function toggleSymptom(s) {
    setSymptoms(prev => prev.includes(s) ? prev.filter(x => x !== s) : [...prev, s]);
  }

  async function handleSubmit() {
    if (!animal)  return setError("Please select an animal.");
    if (!image)   return setError("Please upload an image.");
    setLoading(true);
    setError("");
    try {
      const form = new FormData();
      form.append("image", image);
      form.append("animal", animal);
      symptoms.forEach(s => form.append("symptoms", s));
      const res = await axios.post("http://localhost:5000/predict", form);
      onResults(res.data, { animal, symptoms, image: preview });
    } catch (err) {
      const msg = err.response?.data?.message || "Something went wrong. Please try again.";
      setError(msg);
    }
    setLoading(false);
  }

  return (
    <div style={styles.page}>
      <div style={styles.blob1} />
      <div style={styles.blob2} />

      {loading && <LoadingOverlay animal={animal} />}

      <div style={styles.container}>
        <div style={styles.header}>
          <h2 style={styles.title}>Diagnose Your Animal</h2>
          <p style={styles.sub}>Select the animal, upload a photo, and optionally describe symptoms.</p>
        </div>

        {/* Step 1: Animal */}
        <div style={styles.card}>
          <div style={styles.stepLabel}><span style={styles.stepNum}>1</span> Select Animal</div>
          <div style={styles.animalGrid}>
            {[
              { key: "dog",     emoji: "🐕", label: "Dog" },
              { key: "cow",     emoji: "🐄", label: "Cow" },
              { key: "chicken", emoji: "🐔", label: "Chicken" },
            ].map(a => (
              <button key={a.key}
                style={{ ...styles.animalBtn, ...(animal === a.key ? styles.animalBtnActive : {}) }}
                onClick={() => handleAnimal(a.key)}>
                <span style={{ fontSize: 32 }}>{a.emoji}</span>
                <span style={{ fontFamily: "'Playfair Display', serif", fontSize: 15 }}>{a.label}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Step 2: Image */}
        <div style={styles.card}>
          <div style={styles.stepLabel}><span style={styles.stepNum}>2</span> Upload Photo</div>
          <div style={styles.uploadBox}
            onClick={() => fileRef.current.click()}
            onDragOver={e => e.preventDefault()}
            onDrop={e => { e.preventDefault(); const f = e.dataTransfer.files[0]; if(f){ setImage(f); setPreview(URL.createObjectURL(f)); }}}>
            <input ref={fileRef} type="file" accept="image/*" hidden onChange={handleImage} />
            {preview ? (
              <div style={{ position: "relative" }}>
                <img src={preview} alt="preview" style={styles.preview} />
                <div style={styles.changeBtn}>Click to change</div>
              </div>
            ) : (
              <div style={styles.uploadPlaceholder}>
                <span style={{ fontSize: 48 }}>📸</span>
                <p style={{ fontWeight: 500, color: "#8a7650", marginTop: 8 }}>Drop image here or click to browse</p>
                <p style={{ fontSize: 13, color: "#a09070", marginTop: 4 }}>JPG, PNG supported</p>
              </div>
            )}
          </div>
        </div>

        {/* Step 3: Symptoms */}
        {animal && (
          <div style={{ ...styles.card, animation: "fadeUp 0.5s ease forwards" }}>
            <div style={styles.stepLabel}>
              <span style={styles.stepNum}>3</span> Symptoms
              <span style={styles.optional}>optional</span>
            </div>
            <div style={styles.symptomGrid}>
              {SYMPTOMS[animal].map(s => (
                <button key={s}
                  style={{ ...styles.symptomBtn, ...(symptoms.includes(s) ? styles.symptomBtnActive : {}) }}
                  onClick={() => toggleSymptom(s)}>
                  {symptoms.includes(s) ? "✓ " : ""}{s}
                </button>
              ))}
            </div>
          </div>
        )}

        {error && <div style={styles.error}>⚠️ {error}</div>}

        <button style={styles.submitBtn} onClick={handleSubmit}
          onMouseEnter={e => e.target.style.transform = "scale(1.02)"}
          onMouseLeave={e => e.target.style.transform = "scale(1)"}>
          Analyze Now ✦
        </button>
      </div>
    </div>
  );
}

function LoadingOverlay({ animal }) {
  const msgs = [
    "Scanning the image...",
    "Running disease detection...",
    "Generating heatmap...",
    "Almost there...",
  ];
  const [msgIdx] = useState(0);
  const emojis = { dog: "🐕", cow: "🐄", chicken: "🐔" };

  return (
    <div style={styles.overlay}>
      <div style={styles.overlayCard}>
        <div style={{ fontSize: 64, animation: "float 2s ease-in-out infinite" }}>
          {emojis[animal] || "🔍"}
        </div>
        <div style={styles.spinner} />
        <p style={{ fontFamily: "'Playfair Display', serif", fontSize: 22, color: "#3d3526", marginTop: 16 }}>
          Analyzing...
        </p>
        <p style={{ color: "#8a7650", fontSize: 14, animation: "pulse 2s infinite" }}>
          {msgs[msgIdx]}
        </p>
      </div>
    </div>
  );
}

const styles = {
  page: {
    minHeight: "100vh",
    background: "linear-gradient(135deg, #ece7d1 0%, #fdfaf4 60%, #e8e0cc 100%)",
    padding: "40px 20px",
    position: "relative",
    overflow: "hidden",
  },
  blob1: {
    position: "fixed", top: -100, left: -100,
    width: 300, height: 300,
    background: "rgba(244,194,194,0.15)",
    borderRadius: "60% 40% 30% 70%",
    animation: "blob 8s ease-in-out infinite",
    zIndex: 0,
  },
  blob2: {
    position: "fixed", bottom: -80, right: -80,
    width: 280, height: 280,
    background: "rgba(142,151,125,0.12)",
    borderRadius: "30% 60% 70% 40%",
    animation: "blob 10s ease-in-out infinite reverse",
    zIndex: 0,
  },
  container: {
    maxWidth: 560,
    margin: "0 auto",
    display: "flex",
    flexDirection: "column",
    gap: 20,
    position: "relative",
    zIndex: 1,
  },
  header: { textAlign: "center", marginBottom: 8 },
  title: { fontSize: 36, color: "#3d3526", marginBottom: 8 },
  sub: { color: "#6b5f45", fontSize: 14, fontWeight: 300 },
  card: {
    background: "rgba(253,250,244,0.88)",
    backdropFilter: "blur(16px)",
    borderRadius: 24,
    padding: "28px 28px",
    border: "1px solid rgba(138,118,80,0.12)",
    boxShadow: "0 4px 24px rgba(138,118,80,0.1)",
  },
  stepLabel: {
    display: "flex",
    alignItems: "center",
    gap: 10,
    fontWeight: 500,
    fontSize: 15,
    color: "#3d3526",
    marginBottom: 18,
  },
  stepNum: {
    width: 28, height: 28,
    background: "linear-gradient(135deg, #8a7650, #a08a62)",
    color: "#fdfaf4",
    borderRadius: "50%",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: 13,
    fontWeight: 600,
    flexShrink: 0,
  },
  optional: {
    marginLeft: "auto",
    fontSize: 11,
    color: "#a09070",
    background: "rgba(244,194,194,0.4)",
    padding: "2px 10px",
    borderRadius: 10,
  },
  animalGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(3, 1fr)",
    gap: 12,
  },
  animalBtn: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    gap: 6,
    padding: "18px 12px",
    borderRadius: 16,
    border: "2px solid rgba(138,118,80,0.15)",
    background: "rgba(236,231,209,0.4)",
    cursor: "pointer",
    transition: "all 0.2s",
    color: "#3d3526",
  },
  animalBtnActive: {
    border: "2px solid #8a7650",
    background: "rgba(138,118,80,0.1)",
    boxShadow: "0 0 0 3px rgba(138,118,80,0.1)",
  },
  uploadBox: {
    border: "2px dashed rgba(138,118,80,0.3)",
    borderRadius: 16,
    padding: 24,
    textAlign: "center",
    cursor: "pointer",
    transition: "all 0.2s",
    background: "rgba(236,231,209,0.2)",
    minHeight: 160,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
  },
  uploadPlaceholder: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
  },
  preview: {
    width: "100%",
    maxHeight: 260,
    objectFit: "cover",
    borderRadius: 12,
  },
  changeBtn: {
    position: "absolute",
    bottom: 8, right: 8,
    background: "rgba(138,118,80,0.85)",
    color: "#fdfaf4",
    padding: "4px 12px",
    borderRadius: 8,
    fontSize: 12,
  },
  symptomGrid: {
    display: "flex",
    flexWrap: "wrap",
    gap: 8,
  },
  symptomBtn: {
    padding: "7px 14px",
    borderRadius: 20,
    border: "1px solid rgba(138,118,80,0.2)",
    background: "rgba(236,231,209,0.4)",
    fontSize: 13,
    cursor: "pointer",
    transition: "all 0.2s",
    color: "#5a5240",
  },
  symptomBtnActive: {
    background: "rgba(244,194,194,0.6)",
    border: "1px solid rgba(244,194,194,0.8)",
    color: "#8a7650",
    fontWeight: 500,
  },
  error: {
    background: "rgba(244,194,194,0.3)",
    border: "1px solid rgba(244,194,194,0.6)",
    borderRadius: 12,
    padding: "12px 16px",
    fontSize: 14,
    color: "#8a4040",
  },
  submitBtn: {
    background: "linear-gradient(135deg, #8a7650, #a08a62)",
    color: "#fdfaf4",
    border: "none",
    borderRadius: 16,
    padding: "18px 40px",
    fontSize: 17,
    fontFamily: "'Playfair Display', serif",
    cursor: "pointer",
    transition: "transform 0.2s, box-shadow 0.2s",
    boxShadow: "0 4px 20px rgba(138,118,80,0.35)",
    width: "100%",
    marginBottom: 20,
  },
  overlay: {
    position: "fixed",
    inset: 0,
    background: "rgba(236,231,209,0.85)",
    backdropFilter: "blur(12px)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    zIndex: 100,
  },
  overlayCard: {
    background: "rgba(253,250,244,0.95)",
    borderRadius: 28,
    padding: "48px 56px",
    textAlign: "center",
    boxShadow: "0 8px 40px rgba(138,118,80,0.2)",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    gap: 8,
  },
  spinner: {
    width: 40, height: 40,
    border: "3px solid rgba(138,118,80,0.2)",
    borderTop: "3px solid #8a7650",
    borderRadius: "50%",
    animation: "spin 0.8s linear infinite",
    marginTop: 8,
  },
};