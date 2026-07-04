export default function SimilarityMeter() {
  const percent = 87;

  return (
    <div className="similarity-card">
      <div className="circle">
        <svg width="120" height="120">
          <circle cx="60" cy="60" r="50" stroke="#e5e7eb" strokeWidth="10" fill="none" />
          <circle
            cx="60"
            cy="60"
            r="50"
            stroke="#1E293B"
            strokeWidth="10"
            fill="none"
            strokeDasharray="314"
            strokeDashoffset={314 - (314 * percent) / 100}
          />
        </svg>

        <div className="percent">{percent}%</div>
      </div>

      <p>Case Similarity Score</p>
    </div>
  );
}