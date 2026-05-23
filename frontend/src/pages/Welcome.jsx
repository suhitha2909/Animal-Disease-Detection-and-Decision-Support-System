export default function Welcome({ onStart }) {
  return (
    <div style={styles.page}>

      {/* Background blobs */}
      <div style={styles.blob1} />
      <div style={styles.blob2} />
      <div style={styles.blob3} />

      <div style={styles.container}>

        {/* Floating animal emojis */}
        <div style={styles.floatRow}>
          <span style={{ ...styles.emoji, animationDelay: "0s"   }}>🐕</span>
          <span style={{ ...styles.emoji, animationDelay: "0.4s" }}>🐄</span>
          <span style={{ ...styles.emoji, animationDelay: "0.8s" }}>🐔</span>
        </div>

        <div style={{ ...styles.card, animation: "fadeUp 0.8s ease forwards" }}>
          <div style={styles.badge}>AI-Powered Veterinary Assistant</div>

          <h1 style={styles.title}>
            VetScan
            <span style={styles.titleAccent}> AI</span>
          </h1>

          <p style={styles.subtitle}>
            Upload a photo of your animal and let our AI detect possible diseases instantly —
            with visual explanations and actionable advice.
          </p>

          <div style={styles.features}>
            {[
              { icon: "🔬", text: "Deep Learning Diagnosis" },
              { icon: "🗺️", text: "Visual Heatmap Explanation" },
              { icon: "💬", text: "Symptom-Based Refinement" },
            ].map((f, i) => (
              <div key={i} style={styles.feature}>
                <span style={styles.featureIcon}>{f.icon}</span>
                <span style={styles.featureText}>{f.text}</span>
              </div>
            ))}
          </div>

          <button style={styles.btn} onClick={onStart}
            onMouseEnter={e => e.target.style.transform = "scale(1.04)"}
            onMouseLeave={e => e.target.style.transform = "scale(1)"}>
            Start Diagnosis ✦
          </button>

          <p style={styles.disclaimer}>
            🩺 For informational purposes only. Always consult a veterinarian.
          </p>
        </div>

        {/* Animal cards */}
        <div style={styles.animalRow}>
          {[
            { emoji: "🐕", name: "Dogs",    desc: "4 conditions" },
            { emoji: "🐄", name: "Cattle",  desc: "3 conditions" },
            { emoji: "🐔", name: "Poultry", desc: "4 conditions" },
          ].map((a, i) => (
            <div key={i} style={{ ...styles.animalCard, animationDelay: `${i * 0.15}s`, animation: "fadeUp 0.8s ease forwards", opacity: 0 }}>
              <span style={{ fontSize: 36 }}>{a.emoji}</span>
              <strong style={{ fontFamily: "'Playfair Display', serif", fontSize: 16 }}>{a.name}</strong>
              <span style={{ fontSize: 12, color: "#8a7650", fontWeight: 500 }}>{a.desc}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

const styles = {
  page: {
    minHeight: "100vh",
    background: "linear-gradient(135deg, #ece7d1 0%, #fdfaf4 50%, #e8e0cc 100%)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    position: "relative",
    overflow: "hidden",
    padding: "40px 20px",
  },
  blob1: {
    position: "absolute", top: "-100px", left: "-100px",
    width: 350, height: 350,
    background: "rgba(138,118,80,0.12)",
    borderRadius: "60% 40% 30% 70% / 60% 30% 70% 40%",
    animation: "blob 8s ease-in-out infinite",
  },
  blob2: {
    position: "absolute", bottom: "-80px", right: "-80px",
    width: 300, height: 300,
    background: "rgba(142,151,125,0.15)",
    borderRadius: "30% 60% 70% 40% / 50% 60% 30% 60%",
    animation: "blob 10s ease-in-out infinite reverse",
  },
  blob3: {
    position: "absolute", top: "40%", right: "10%",
    width: 200, height: 200,
    background: "rgba(244,194,194,0.2)",
    borderRadius: "50% 30% 60% 40%",
    animation: "blob 12s ease-in-out infinite",
  },
  container: {
    maxWidth: 560,
    width: "100%",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    gap: 24,
    position: "relative",
    zIndex: 1,
  },
  floatRow: {
    display: "flex",
    gap: 24,
    marginBottom: 8,
  },
  emoji: {
    fontSize: 42,
    display: "inline-block",
    animation: "float 3s ease-in-out infinite",
    filter: "drop-shadow(0 4px 8px rgba(0,0,0,0.1))",
  },
  card: {
    background: "rgba(253,250,244,0.85)",
    backdropFilter: "blur(20px)",
    borderRadius: 28,
    padding: "44px 40px",
    textAlign: "center",
    boxShadow: "0 8px 40px rgba(138,118,80,0.15), 0 2px 8px rgba(0,0,0,0.06)",
    border: "1px solid rgba(138,118,80,0.15)",
    width: "100%",
  },
  badge: {
    display: "inline-block",
    background: "rgba(244,194,194,0.5)",
    color: "#8a7650",
    border: "1px solid rgba(244,194,194,0.8)",
    borderRadius: 20,
    padding: "5px 16px",
    fontSize: 12,
    fontWeight: 500,
    letterSpacing: "0.05em",
    marginBottom: 20,
  },
  title: {
    fontSize: 52,
    fontWeight: 600,
    color: "#3d3526",
    lineHeight: 1.1,
    marginBottom: 16,
  },
  titleAccent: {
    color: "#8a7650",
    fontStyle: "italic",
  },
  subtitle: {
    fontSize: 15,
    lineHeight: 1.7,
    color: "#6b5f45",
    marginBottom: 28,
    fontWeight: 300,
  },
  features: {
    display: "flex",
    flexDirection: "column",
    gap: 10,
    marginBottom: 32,
    textAlign: "left",
  },
  feature: {
    display: "flex",
    alignItems: "center",
    gap: 12,
    background: "rgba(142,151,125,0.08)",
    borderRadius: 12,
    padding: "10px 16px",
    border: "1px solid rgba(142,151,125,0.15)",
  },
  featureIcon: { fontSize: 18 },
  featureText: { fontSize: 14, color: "#5a5240", fontWeight: 400 },
  btn: {
    background: "linear-gradient(135deg, #8a7650, #a08a62)",
    color: "#fdfaf4",
    border: "none",
    borderRadius: 16,
    padding: "16px 40px",
    fontSize: 16,
    fontWeight: 500,
    cursor: "pointer",
    letterSpacing: "0.03em",
    transition: "transform 0.2s, box-shadow 0.2s",
    boxShadow: "0 4px 20px rgba(138,118,80,0.35)",
    width: "100%",
    marginBottom: 16,
    fontFamily: "'Playfair Display', serif",
  },
  disclaimer: {
    fontSize: 12,
    color: "#a09070",
    fontWeight: 300,
  },
  animalRow: {
    display: "flex",
    gap: 16,
    width: "100%",
  },
  animalCard: {
    flex: 1,
    background: "rgba(253,250,244,0.7)",
    borderRadius: 20,
    padding: "20px 16px",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    gap: 6,
    border: "1px solid rgba(138,118,80,0.12)",
    boxShadow: "0 4px 16px rgba(138,118,80,0.08)",
    opacity: 0,
  },
};