type SurveySummaryProps = {
  summary: Record<string, number>;
};

const traitMap: Record<string, string> = {
  O: "Open-Mindedness",
  C: "Conscientiousness",
  E: "Extraversion",
  A: "Agreeableness",
  N: "Neuroticism",
};

export default function SurveySummary({ summary }: SurveySummaryProps) {
  if (!summary || Object.keys(summary).length === 0) {
    return null;
  }

  return (
    <div className="summary">
      {Object.entries(summary).map(([code, value]) => (
        <div key={code} className="summary__row">
          <div>
            <p className="summary__label">{traitMap[code] ?? code}</p>
            <span className="summary__value">{value.toFixed(2)}</span>
          </div>
          <div className="summary__bar">
            <div
              className="summary__fill"
              style={{ width: `${(value / 5) * 100}%` }}
            />
          </div>
        </div>
      ))}
    </div>
  );
}
