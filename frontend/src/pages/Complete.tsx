import { useLocation, useNavigate } from "react-router-dom";

const traitMap: Record<string, string> = {
  O: "Open-Mindedness",
  C: "Conscientiousness",
  E: "Extraversion",
  A: "Agreeableness",
  N: "Neuroticism",
};

export default function Complete() {
  const location = useLocation();
  const navigate = useNavigate();
  const scored = (
    location.state as { scored?: { summary?: Record<string, number> } } | null
  )?.scored;
  const summary = scored?.summary ?? {};

  return (
    <section className="panel">
      <div className="panel__body">
        <h2>Survey complete</h2>
        <p className="panel__lead">
          Thank you for finishing the baseline questionnaire. Your responses have been
          recorded securely.
        </p>

        {Object.keys(summary).length > 0 && (
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
        )}

        <button
          className="secondary"
          type="button"
          onClick={() => navigate("/")}
        >
          Return to start
        </button>
      </div>
    </section>
  );
}
