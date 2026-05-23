import { useState } from "react";
import axios from "axios";

const DISEASE_INFO = {
  healthy: {
    icon: "✅",
    title: "Healthy",
    desc: "No disease detected. Your animal appears to be in good health based on the image analysis.",
    tips: ["Continue regular veterinary checkups.", "Maintain a balanced diet and clean living environment."],
  },
  skin_disease: {
    icon: "🩹",
    title: "Skin Disease",
    desc: "A general skin condition has been detected. This may include mange, dermatitis, or other dermatological issues.",
    tips: ["Keep the affected area clean and dry.", "Consult a vet for proper diagnosis and medicated treatment."],
  },
  bacterial_dermatitis: {
    icon: "🦠",
    title: "Bacterial Dermatitis",
    desc: "A bacterial skin infection that causes inflammation, redness, and possible discharge on the skin.",
    tips: ["Avoid letting the dog lick or scratch the area.", "A vet may prescribe antibiotics or medicated shampoo."],
  },
  fungal_infection: {
    icon: "🍄",
    title: "Fungal Infection",
    desc: "A fungal condition such as ringworm causing circular bald patches and scaling on the skin.",
    tips: ["Isolate from other pets as ringworm is contagious.", "Antifungal medication prescribed by a vet is essential."],
  },
  lumpy_skin: {
    icon: "🔴",
    title: "Lumpy Skin Disease",
    desc: "A viral disease causing nodular lesions on the skin. Common in cattle and can spread through insects.",
    tips: ["Isolate the affected animal from the herd immediately.", "Contact a vet for antiviral and supportive treatment."],
  },
  foot_mouth_disease: {
    icon: "🦶",
    title: "Foot & Mouth Disease",
    desc: "A highly contagious viral disease causing blisters on feet and mouth. Affects cattle and other livestock.",
    tips: ["Quarantine the animal and report to local livestock authority.", "Seek immediate veterinary care — this is a notifiable disease."],
  },
  newcastle: {
    icon: "🐦",
    title: "Newcastle Disease",
    desc: "A serious viral disease in poultry causing neurological symptoms, respiratory distress, and high mortality.",
    tips: ["Isolate sick birds immediately to prevent flock spread.", "Contact a vet — vaccination of remaining flock may be recommended."],
  },
  coccidiosis: {
    icon: "🩸",
    title: "Coccidiosis",
    desc: "A parasitic intestinal disease causing bloody droppings, lethargy, and weight loss in poultry.",
    tips: ["Provide clean water and improve litter hygiene.", "Anticoccidial medication from a vet is usually effective."],
  },
  salmonella: {
    icon: "⚠️",
    title: "Salmonella Infection",
    desc: "A bacterial infection causing weakness, diarrhea, and drooping wings. Can spread to humans.",
    tips: ["Practice strict hygiene when handling affected birds.", "Consult a vet for appropriate antibiotic treatment."],
  },
};

const RISK_STYLE = {
  HIGH:   { bg: "rgba(220,80,80,0.1)",  border: "rgba(220,80,80,0.3)",  color: "#c04040", label: "High Risk" },
  MEDIUM: { bg: "rgba(210,150,50,0.1)", border: "rgba(210,150,50,0.3)", color: "#a07030", label: "Medium Risk" },
  LOW:    { bg: "rgba(100,170,100,0.1)",border: "rgba(100,170,100,0.3)",color: "#406040", label: "Low Risk" },
};

export default function Results({ data, input, onBack }) {
  const [answers,  setAnswers]  = useState({});
  const [refined,  setRefined]  = useState(null);
  const [refining, setRefining] = useState(false);
  const [showAll,  setShowAll]  = useState(false);

  const top     = data.predictions[0];
  const info    = DISEASE_INFO[top.disease] || { icon: "🔍", title: top.disease, desc: "Detected condition.", tips: ["Consult a veterinarian."] };
  const risk    = refined ? RISK_STYLE[refined.risk_level] : null;
  const display = refined || top;

  async function handleRefine() {
    setRefining(true);
    try {
      const res = await axios.post("http://localhost:5000/refine", {
        top_prediction: top,
        symptoms: input.symptoms,
        answers,
      });
      setRefined(res.data);
    } catch (e) {
      console.error(e);
    }
    setRefining(false);
  }

  const allAnswered = data.followup_questions.length > 0 &&
    data.followup_questions.every(q => answers[q]);

  return (
    <div style={styles.page}>
      <div style={styles.blob1} />
      <div style={styles.blob2} />

      <div style={styles.container}>

        {/* Header */}
        <div style={styles.header}>
          <button style={styles.backBtn} onClick={onBack}>← Back</button>
          <h2 style={styles.title}>Diagnosis Results</h2>
          <p style={styles.sub}>Analysis complete for your {data.detected_animal}</p>
        </div>

        {/* Top prediction */}
        <div style={{ ...styles.card, borderTop: "4px solid #8a7650" }}>
          <div style={styles.diseaseHeader}>
            <span style={{ fontSize: 36 }}>{info.icon}</span>
            <div>
              <div style={styles.diseaseTitle}>{info.title}</div>
              <div style={styles.animalTag}>
                {data.detected_animal === "dog" ? "🐕" : data.detected_animal === "cow" ? "🐄" : "🐔"}
                {" "}{data.detected_animal}
              </div>
            </div>
            <div style={styles.confidencePill}>
              {top.confidence.toFixed(1)}%
            </div>
          </div>
          <p style={styles.diseaseDesc}>{info.desc}</p>

          {/* Confidence bar */}
          <div style={styles.barBg}>
            <div style={{ ...styles.barFill, width: `${top.confidence}%` }} />
          </div>
          <div style={styles.barLabel}>Model confidence</div>
        </div>

        {/* Grad-CAM */}
        {data.heatmap && (
          <div style={styles.card}>
            <div style={styles.sectionTitle}>🗺️ Where the AI looked</div>
            <p style={{ fontSize: 13, color: "#8a7650", marginBottom: 12 }}>
              Red/yellow areas show the regions that influenced the prediction most.
            </p>
            <div style={styles.heatmapRow}>
              <div style={{ flex: 1 }}>
                <p style={styles.imgLabel}>Original</p>
                <img src={input.image} alt="original" style={styles.heatmapImg} />
              </div>
              <div style={{ flex: 1 }}>
                <p style={styles.imgLabel}>AI Focus Map</p>
                <img src={`data:image/jpeg;base64,${data.heatmap}`} alt="heatmap" style={styles.heatmapImg} />
              </div>
            </div>
          </div>
        )}

        {/* Tips */}
        <div style={styles.card}>
          <div style={styles.sectionTitle}>💡 Recommendations</div>
          {info.tips.map((tip, i) => (
            <div key={i} style={styles.tip}>
              <span style={styles.tipNum}>{i + 1}</span>
              <span style={{ fontSize: 14, color: "#5a5240" }}>{tip}</span>
            </div>
          ))}
        </div>

        {/* Other predictions */}
        {data.predictions.length > 1 && (
          <div style={styles.card}>
            <div style={{ ...styles.sectionTitle, cursor: "pointer" }} onClick={() => setShowAll(!showAll)}>
              📊 Other possibilities {showAll ? "▲" : "▼"}
            </div>
            {showAll && data.predictions.slice(1).map((p, i) => (
              <div key={i} style={styles.altPred}>
                <span style={{ fontSize: 13, color: "#5a5240" }}>
                  {DISEASE_INFO[p.disease]?.title || p.disease}
                </span>
                <span style={{ fontSize: 13, color: "#8a7650", fontWeight: 500 }}>
                  {p.confidence.toFixed(1)}%
                </span>
              </div>
            ))}
          </div>
        )}

        {/* Follow-up questions */}
        {!refined && data.followup_questions.length > 0 && (
          <div style={styles.card}>
            <div style={styles.sectionTitle}>❓ Follow-up Questions</div>
            <p style={{ fontSize: 13, color: "#8a7650", marginBottom: 16 }}>
              Answer these to refine the diagnosis confidence score.
            </p>
            {data.followup_questions.map((q, i) => (
              <div key={i} style={styles.qBlock}>
                <p style={styles.qText}>{q}</p>
                <div style={styles.qBtns}>
                  {["yes", "no"].map(v => (
                    <button key={v}
                      style={{ ...styles.qBtn, ...(answers[q] === v ? styles.qBtnActive : {}) }}
                      onClick={() => setAnswers(a => ({ ...a, [q]: v }))}>
                      {v === "yes" ? "✓ Yes" : "✗ No"}
                    </button>
                  ))}
                </div>
              </div>
            ))}
            {allAnswered && (
              <button style={styles.refineBtn} onClick={handleRefine} disabled={refining}>
                {refining ? "Refining..." : "Get Refined Diagnosis ✦"}
              </button>
            )}
          </div>
        )}

        {/* Refined result */}
        {refined && risk && (
          <div style={{ ...styles.card, background: risk.bg, border: `1px solid ${risk.border}` }}>
            <div style={styles.sectionTitle}>✦ Refined Diagnosis</div>
            <div style={styles.refinedRow}>
              <div>
                <div style={{ fontSize: 13, color: "#6b5f45" }}>Final Confidence</div>
                <div style={{ fontSize: 28, fontFamily: "'Playfair Display', serif", color: "#3d3526" }}>
                  {refined.confidence}%
                </div>
              </div>
              <div style={{ ...styles.riskBadge, background: risk.bg, color: risk.color, border: `1px solid ${risk.border}` }}>
                {risk.label}
              </div>
            </div>
            <p style={{ fontSize: 14, color: "#5a5240", marginTop: 12, lineHeight: 1.6 }}>
              {refined.advice}
            </p>
          </div>
        )}

        <button style={styles.newBtn} onClick={onBack}>
          + Start New Diagnosis
        </button>

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
    position: "fixed", top: -80, right: -80,
    width: 280, height: 280,
    background: "rgba(244,194,194,0.15)",
    borderRadius: "60% 40% 30% 70%",
    animation: "blob 8s ease-in-out infinite",
    zIndex: 0,
  },
  blob2: {
    position: "fixed", bottom: -60, left: -60,
    width: 240, height: 240,
    background: "rgba(142,151,125,0.12)",
    borderRadius: "30% 60% 70% 40%",
    animation: "blob 10s ease-in-out infinite reverse",
    zIndex: 0,
  },
  container: {
    maxWidth: 580,
    margin: "0 auto",
    display: "flex",
    flexDirection: "column",
    gap: 20,
    position: "relative",
    zIndex: 1,
  },
  header: { textAlign: "center", marginBottom: 4 },
  backBtn: {
    background: "rgba(138,118,80,0.1)",
    border: "1px solid rgba(138,118,80,0.2)",
    borderRadius: 10,
    padding: "6px 16px",
    fontSize: 13,
    cursor: "pointer",
    color: "#8a7650",
    marginBottom: 12,
    fontFamily: "'DM Sans', sans-serif",
  },
  title: { fontSize: 34, color: "#3d3526", marginBottom: 6 },
  sub:   { color: "#8a7650", fontSize: 14, fontWeight: 300, textTransform: "capitalize" },
  card: {
    background: "rgba(253,250,244,0.88)",
    backdropFilter: "blur(16px)",
    borderRadius: 24,
    padding: "24px 28px",
    border: "1px solid rgba(138,118,80,0.12)",
    boxShadow: "0 4px 24px rgba(138,118,80,0.1)",
    animation: "fadeUp 0.6s ease forwards",
  },
  diseaseHeader: {
    display: "flex",
    alignItems: "center",
    gap: 16,
    marginBottom: 16,
  },
  diseaseTitle: {
    fontFamily: "'Playfair Display', serif",
    fontSize: 22,
    color: "#3d3526",
  },
  animalTag: {
    fontSize: 12,
    color: "#8a7650",
    textTransform: "capitalize",
    marginTop: 2,
  },
  confidencePill: {
    marginLeft: "auto",
    background: "linear-gradient(135deg, #8a7650, #a08a62)",
    color: "#fdfaf4",
    borderRadius: 20,
    padding: "6px 16px",
    fontSize: 15,
    fontWeight: 600,
    flexShrink: 0,
  },
  diseaseDesc: {
    fontSize: 14,
    color: "#6b5f45",
    lineHeight: 1.7,
    marginBottom: 16,
  },
  barBg: {
    height: 6,
    background: "rgba(138,118,80,0.15)",
    borderRadius: 10,
    overflow: "hidden",
  },
  barFill: {
    height: "100%",
    background: "linear-gradient(90deg, #8a7650, #a08a62)",
    borderRadius: 10,
    transition: "width 1s ease",
  },
  barLabel: {
    fontSize: 11,
    color: "#a09070",
    marginTop: 4,
  },
  sectionTitle: {
    fontFamily: "'Playfair Display', serif",
    fontSize: 17,
    color: "#3d3526",
    marginBottom: 14,
  },
  heatmapRow: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: 12,
  },
  imgLabel: {
    fontSize: 12,
    color: "#8a7650",
    marginBottom: 6,
    fontWeight: 500,
  },
  heatmapImg: {
    width: "100%",
    borderRadius: 12,
    objectFit: "cover",
    maxHeight: 180,
  },
  tip: {
    display: "flex",
    alignItems: "flex-start",
    gap: 12,
    marginBottom: 10,
    padding: "10px 14px",
    background: "rgba(244,194,194,0.2)",
    borderRadius: 12,
    border: "1px solid rgba(244,194,194,0.4)",
  },
  tipNum: {
    width: 22, height: 22,
    background: "rgba(244,194,194,0.6)",
    borderRadius: "50%",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: 12,
    fontWeight: 600,
    color: "#8a7650",
    flexShrink: 0,
  },
  altPred: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "10px 14px",
    background: "rgba(236,231,209,0.4)",
    borderRadius: 10,
    marginBottom: 8,
  },
  qBlock: {
    marginBottom: 16,
    padding: "14px 16px",
    background: "rgba(236,231,209,0.3)",
    borderRadius: 14,
  },
  qText: {
    fontSize: 14,
    color: "#3d3526",
    marginBottom: 10,
    lineHeight: 1.5,
  },
  qBtns: { display: "flex", gap: 8 },
  qBtn: {
    flex: 1,
    padding: "8px",
    borderRadius: 10,
    border: "1px solid rgba(138,118,80,0.2)",
    background: "rgba(236,231,209,0.4)",
    fontSize: 13,
    cursor: "pointer",
    color: "#5a5240",
    transition: "all 0.2s",
    fontFamily: "'DM Sans', sans-serif",
  },
  qBtnActive: {
    background: "rgba(244,194,194,0.5)",
    border: "1px solid rgba(244,194,194,0.7)",
    color: "#8a4050",
    fontWeight: 500,
  },
  refineBtn: {
    width: "100%",
    padding: "14px",
    background: "linear-gradient(135deg, #8e977d, #a0a88e)",
    color: "#fdfaf4",
    border: "none",
    borderRadius: 14,
    fontSize: 15,
    fontFamily: "'Playfair Display', serif",
    cursor: "pointer",
    marginTop: 8,
    boxShadow: "0 4px 16px rgba(142,151,125,0.3)",
  },
  refinedRow: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
  },
  riskBadge: {
    padding: "8px 20px",
    borderRadius: 20,
    fontSize: 14,
    fontWeight: 600,
  },
  newBtn: {
    width: "100%",
    padding: "16px",
    background: "transparent",
    color: "#8a7650",
    border: "2px solid rgba(138,118,80,0.3)",
    borderRadius: 16,
    fontSize: 15,
    fontFamily: "'Playfair Display', serif",
    cursor: "pointer",
    marginBottom: 40,
    transition: "all 0.2s",
  },
};