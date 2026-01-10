import { useLocation, useNavigate } from "react-router-dom";
import SurveySummary from "../components/SurveySummary";

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

        <SurveySummary summary={summary} />

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
