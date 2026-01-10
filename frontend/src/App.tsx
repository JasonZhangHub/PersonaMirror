import { useMemo, useState } from "react";
import { Navigate, Route, Routes } from "react-router-dom";
import Login from "./pages/Login";
import Consent from "./pages/Consent";
import Survey from "./pages/Survey";
import Complete from "./pages/Complete";
import { clearUser, loadUser, saveUser } from "./storage";
import type { User } from "./types";

export default function App() {
  const [user, setUser] = useState<User | null>(() => loadUser());

  const isConsented = useMemo(() => {
    return Boolean(user?.consent_signed_at);
  }, [user]);

  const handleUserChange = (next: User | null) => {
    setUser(next);
    if (next) {
      saveUser(next);
    } else {
      clearUser();
    }
  };

  return (
    <div className="app">
      <header className="app__header">
        <div>
          <h1>Reflection Lab</h1>
          <p className="app__subtitle">
            Help us study how collaboration with AI teams shapes self-perceived personality.
          </p>
        </div>
        <div className="app__status">
          <span>{user ? `Participant ${user.participant_id}` : "Not signed in"}</span>
          {user && (
            <button
              className="link-button"
              type="button"
              onClick={() => handleUserChange(null)}
            >
              Sign out
            </button>
          )}
        </div>
      </header>

      <main className="app__main">
        <Routes>
          <Route path="/" element={<Login onLogin={handleUserChange} />} />
          <Route
            path="/consent"
            element={
              user ? (
                <Consent user={user} onUpdate={handleUserChange} />
              ) : (
                <Navigate to="/" replace />
              )
            }
          />
          <Route
            path="/survey"
            element={
              user && isConsented ? (
                <Survey user={user} />
              ) : (
                <Navigate to="/consent" replace />
              )
            }
          />
          <Route path="/complete" element={<Complete />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  );
}
