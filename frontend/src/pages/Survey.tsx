import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getQuestions, submitResponses } from "../api";
import ProgressSteps from "../components/ProgressSteps";
import QuestionCard from "../components/QuestionCard";
import type { BFI2Questions, User } from "../types";

const steps = [
  {
    label: "Log in",
    description: "Confirm your participant ID.",
  },
  {
    label: "Consent",
    description: "Share demographics and agree to participate.",
  },
  {
    label: "BFI-2 Survey",
    description: "Complete the personality inventory.",
  },
];

type SurveyProps = {
  user: User;
};

const PAGE_SIZE = 10;

export default function Survey({ user }: SurveyProps) {
  const [questions, setQuestions] = useState<BFI2Questions | null>(null);
  const [responses, setResponses] = useState<Record<number, number>>({});
  const [page, setPage] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    let isActive = true;
    getQuestions()
      .then((data) => {
        if (isActive) {
          setQuestions(data);
        }
      })
      .catch((err) => {
        if (isActive) {
          setError(err instanceof Error ? err.message : "Unable to load survey.");
        }
      });

    return () => {
      isActive = false;
    };
  }, []);

  const items = questions?.items ?? [];
  const totalPages = Math.ceil(items.length / PAGE_SIZE);
  const startIndex = page * PAGE_SIZE;
  const currentItems = items.slice(startIndex, startIndex + PAGE_SIZE);

  const answeredCount = Object.keys(responses).length;
  const progress = items.length ? Math.round((answeredCount / items.length) * 100) : 0;

  const pageComplete = useMemo(() => {
    return currentItems.every((item) => responses[item.id]);
  }, [currentItems, responses]);

  const handleChange = (id: number, value: number) => {
    setResponses((prev) => ({ ...prev, [id]: value }));
  };

  const handleSubmit = async () => {
    if (!questions) {
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const result = await submitResponses(user.id, responses, "pre");
      navigate("/complete", { state: { scored: result.scored } });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to submit responses.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="panel panel--wide">
      <ProgressSteps current={2} steps={steps} />
      <div className="panel__body">
        <div className="panel__split">
          <div>
            <h2>Big Five Inventory-2</h2>
            <p className="panel__lead">
              {questions?.instructions ??
                "Please respond to each statement based on how well it describes you."}
            </p>
          </div>
          <div className="progress">
            <span>{progress}% complete</span>
            <div className="progress__bar">
              <div className="progress__fill" style={{ width: `${progress}%` }} />
            </div>
          </div>
        </div>

        {error && <p className="form__error">{error}</p>}

        {questions ? (
          <div className="question-list">
            {currentItems.map((question) => (
              <QuestionCard
                key={question.id}
                question={question}
                value={responses[question.id]}
                onChange={(value) => handleChange(question.id, value)}
                scale={questions.scale}
              />
            ))}
          </div>
        ) : (
          <p className="panel__lead">Loading survey...</p>
        )}

        <div className="panel__actions">
          <button
            className="secondary"
            type="button"
            disabled={page === 0}
            onClick={() => setPage((prev) => Math.max(0, prev - 1))}
          >
            Previous
          </button>
          {page < totalPages - 1 ? (
            <button
              className="primary"
              type="button"
              disabled={!pageComplete}
              onClick={() => setPage((prev) => Math.min(totalPages - 1, prev + 1))}
            >
              Next
            </button>
          ) : (
            <button
              className="primary"
              type="button"
              disabled={!questions || !pageComplete || loading}
              onClick={handleSubmit}
            >
              {loading ? "Submitting..." : "Submit survey"}
            </button>
          )}
        </div>
      </div>
    </section>
  );
}
