"use client";

import { useState } from "react";
import { Loader2, MessageSquareText } from "lucide-react";

export default function QuestionsPanel({ analysisId, hasGaps }) {
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  if (!hasGaps) return null;

  async function loadQuestions() {
    setLoading(true);
    setError("");

    try {
      const response = await fetch(`/api/interview-questions/${analysisId}`, {
        method: "POST",
      });
      const data = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(data.detail || "Interview questions could not be generated.");
      }
      setQuestions(data.questions || []);
    } catch (requestError) {
      setError(requestError.message || "Could not reach the interview question service.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section aria-labelledby="questions-heading" className="border-t border-line pt-8">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h3 id="questions-heading" className="font-display text-xl font-semibold">
            Practice for your skill gaps
          </h3>
          <p className="mt-1 text-slate">
            Prepare with interview questions based on the skills to build.
          </p>
        </div>
        <button
          type="button"
          onClick={loadQuestions}
          disabled={loading}
          className="inline-flex items-center gap-2 rounded-lg bg-ink px-4 py-2.5 font-medium text-white transition-colors hover:bg-ultramarine disabled:cursor-wait disabled:opacity-70"
        >
          {loading ? <Loader2 size={17} className="animate-spin" aria-hidden /> : <MessageSquareText size={17} aria-hidden />}
          {loading ? "Preparing" : questions.length ? "Refresh questions" : "Generate questions"}
        </button>
      </div>

      {error && <p role="alert" className="mt-4 text-sm text-rose-ink">{error}</p>}
      {questions.length > 0 && (
        <ol className="mt-6 divide-y divide-line border-y border-line">
          {questions.map((item, index) => (
            <li key={`${item.skill}-${index}`} className="grid gap-1 py-4 sm:grid-cols-[10rem_1fr] sm:gap-6">
              <span className="text-sm font-semibold text-ultramarine">{item.skill}</span>
              <span className="leading-relaxed">{item.question}</span>
            </li>
          ))}
        </ol>
      )}
    </section>
  );
}
