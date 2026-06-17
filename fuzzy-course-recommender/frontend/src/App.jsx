import { useState } from "react";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

const fields = [
  {
    key: "math_interest",
    label: "Math interest",
    hint: "Comfort with numbers, logic, and analytical thinking.",
  },
  {
    key: "programming_interest",
    label: "Programming interest",
    hint: "How much you enjoy building things with code.",
  },
  {
    key: "time_availability",
    label: "Time availability",
    hint: "How much time you can realistically dedicate each week.",
  },
  {
    key: "career_clarity",
    label: "Career clarity",
    hint: "How clearly you know the direction you want to pursue.",
  },
];

const initialForm = {
  math_interest: 5,
  programming_interest: 5,
  time_availability: 5,
  career_clarity: 5,
};

export default function App() {
  const [form, setForm] = useState(initialForm);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const onChange = (key, value) => {
    setForm((current) => ({
      ...current,
      [key]: Number(value),
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError("");

    try {
      const response = await fetch(`${API_URL}/recommend`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(form),
      });

      if (!response.ok) {
        throw new Error("The API request failed. Make sure the backend server is running.");
      }

      const data = await response.json();
      setResult(data);
    } catch (submissionError) {
      setError(submissionError.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-shell">
      <main className="app-card">
        <section className="hero">
          <p className="eyebrow">Smart learning path finder</p>
          <h1>Fuzzy Course Recommender</h1>
          <p className="intro">
            Rate your interests from 0 to 10 and let a lightweight fuzzy-logic
            engine suggest the course track that fits you best.
          </p>
        </section>

        <section className="content-grid">
          <form className="panel" onSubmit={handleSubmit}>
            <h2>Your profile</h2>
            <div className="field-list">
              {fields.map((field) => (
                <label className="field" key={field.key}>
                  <div className="field-copy">
                    <span>{field.label}</span>
                    <small>{field.hint}</small>
                  </div>
                  <div className="slider-row">
                    <input
                      type="range"
                      min="0"
                      max="10"
                      step="1"
                      value={form[field.key]}
                      onChange={(event) => onChange(field.key, event.target.value)}
                    />
                    <strong>{form[field.key]}</strong>
                  </div>
                </label>
              ))}
            </div>
            <button type="submit" disabled={loading}>
              {loading ? "Analyzing..." : "Get recommendation"}
            </button>
            {error ? <p className="error">{error}</p> : null}
          </form>

          <section className="panel result-panel">
            <h2>Recommendation</h2>
            {result ? (
              <>
                <div className="result-hero">
                  <p className="result-label">Recommended course</p>
                  <h3>{result.recommended_course}</h3>
                  <p className="result-meta">
                    Suitability: <strong>{result.suitability}</strong>
                  </p>
                </div>

                <div className="metric-grid">
                  <article className="metric">
                    <span>Confidence</span>
                    <strong>{result.confidence}</strong>
                  </article>
                  <article className="metric">
                    <span>Score</span>
                    <strong>{result.score}/10</strong>
                  </article>
                  <article className="metric">
                    <span>Difficulty</span>
                    <strong>{result.difficulty}</strong>
                  </article>
                </div>

                <div className="breakdown">
                  <h4>Course breakdown</h4>
                  {Object.entries(result.course_breakdown).map(([name, value]) => (
                    <div className="breakdown-row" key={name}>
                      <span>{name}</span>
                      <div className="bar-track">
                        <div
                          className="bar-fill"
                          style={{ width: `${Math.max(value, 0.05) * 100}%` }}
                        />
                      </div>
                      <strong>{value}</strong>
                    </div>
                  ))}
                </div>
              </>
            ) : (
              <div className="empty-state">
                <p>Your recommendation will appear here after you submit the form.</p>
              </div>
            )}
          </section>
        </section>
      </main>
    </div>
  );
}
