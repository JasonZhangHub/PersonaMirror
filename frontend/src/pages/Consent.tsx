import { useState } from "react";
import type { FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { updateUser } from "../api";
import ProgressSteps from "../components/ProgressSteps";
import type { User } from "../types";

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

const educationOptions = [
  "High school",
  "Some college",
  "Bachelor's degree",
  "Master's degree",
  "Doctorate",
  "Other",
];

const genderOptions = [
  "Woman",
  "Man",
  "Non-binary",
  "Prefer not to say",
  "Other",
];

type ConsentProps = {
  user: User;
  onUpdate: (user: User) => void;
};

export default function Consent({ user, onUpdate }: ConsentProps) {
  const [alias, setAlias] = useState(user.alias ?? "");
  const [age, setAge] = useState<number | "">(
    typeof user.age === "number" ? user.age : ""
  );
  const [education, setEducation] = useState(user.education ?? "");
  const [gender, setGender] = useState(user.gender ?? "");
  const [consented, setConsented] = useState(Boolean(user.consent_signed_at));
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    if (!consented) {
      setError("You must confirm consent to continue.");
      return;
    }

    setLoading(true);
    try {
      const normalizedAge =
        typeof age === "number" && !Number.isNaN(age) ? age : undefined;
      const updated = await updateUser(user.id, {
        alias: alias.trim() || undefined,
        age: normalizedAge,
        education,
        gender,
        consented: true,
      });
      onUpdate(updated);
      navigate("/survey");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to save consent.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="panel">
      <ProgressSteps current={1} steps={steps} />
      <div className="panel__body">
        <div>
          <h2>Consent and demographics</h2>
          <p className="panel__lead">
            Provide a few details for the study record, then acknowledge consent.
          </p>
        </div>
        <form className="form" onSubmit={handleSubmit}>
          <div className="form__grid">
            <label className="field">
              Name alias
              <input
                type="text"
                value={alias}
                onChange={(event) => setAlias(event.target.value)}
                placeholder="What should we call you?"
                required
              />
            </label>
            <label className="field">
              Age
              <input
                type="number"
                min={18}
                max={120}
                value={age}
                onChange={(event) => {
                  const value = event.target.value;
                  setAge(value === "" ? "" : Number(value));
                }}
                placeholder="18"
                required
              />
            </label>
            <label className="field">
              Education
              <select
                value={education}
                onChange={(event) => setEducation(event.target.value)}
                required
              >
                <option value="" disabled>
                  Select one
                </option>
                {educationOptions.map((option) => (
                  <option key={option} value={option}>
                    {option}
                  </option>
                ))}
              </select>
            </label>
            <label className="field">
              Gender
              <select
                value={gender}
                onChange={(event) => setGender(event.target.value)}
                required
              >
                <option value="" disabled>
                  Select one
                </option>
                {genderOptions.map((option) => (
                  <option key={option} value={option}>
                    {option}
                  </option>
                ))}
              </select>
            </label>
          </div>

          <label className="checkbox">
            <input
              type="checkbox"
              checked={consented}
              onChange={(event) => setConsented(event.target.checked)}
            />
            <span>
              I have read the consent form and agree to participate in this study.
            </span>
          </label>

          {error && <p className="form__error">{error}</p>}
          <button className="primary" type="submit" disabled={loading}>
            {loading ? "Saving..." : "Continue to survey"}
          </button>
        </form>
      </div>
    </section>
  );
}
