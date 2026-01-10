import { useState } from "react";
import type { FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { loginUser, registerUser } from "../api";
import ProgressSteps from "../components/ProgressSteps";
import type { User } from "../types";

type LoginProps = {
  onLogin: (user: User) => void;
};

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

export default function Login({ onLogin }: LoginProps) {
  const [mode, setMode] = useState<"login" | "register">("login");
  const [participantId, setParticipantId] = useState("");
  const [passcode, setPasscode] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const user =
        mode === "login"
          ? await loginUser(participantId.trim(), passcode)
          : await registerUser(participantId.trim(), passcode);
      onLogin(user);
      navigate(user.consent_signed_at ? "/survey" : "/consent");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to continue.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="panel">
      <ProgressSteps current={0} steps={steps} />
      <div className="panel__body">
        <div>
          <h2>{mode === "login" ? "Welcome back" : "Create your participant ID"}</h2>
          <p className="panel__lead">
            {mode === "login"
              ? "Sign in to continue to consent and the BFI-2 survey."
              : "Set a secure passcode. You will use this ID for the full study."}
          </p>
        </div>
        <form className="form" onSubmit={handleSubmit}>
          <label className="field">
            Participant ID
            <input
              type="text"
              value={participantId}
              onChange={(event) => setParticipantId(event.target.value)}
              placeholder="e.g. PM-042"
              required
            />
          </label>
          <label className="field">
            Passcode
            <input
              type="password"
              value={passcode}
              onChange={(event) => setPasscode(event.target.value)}
              placeholder="At least 4 characters"
              required
            />
          </label>
          {error && <p className="form__error">{error}</p>}
          <button className="primary" type="submit" disabled={loading}>
            {loading
              ? "Please wait..."
              : mode === "login"
                ? "Sign in"
                : "Create account"}
          </button>
        </form>
        <div className="panel__footer">
          <span>
            {mode === "login" ? "New to the study?" : "Already have an ID?"}
          </span>
          <button
            className="link-button"
            type="button"
            onClick={() => setMode(mode === "login" ? "register" : "login")}
          >
            {mode === "login" ? "Create an account" : "Sign in instead"}
          </button>
        </div>
      </div>
    </section>
  );
}
