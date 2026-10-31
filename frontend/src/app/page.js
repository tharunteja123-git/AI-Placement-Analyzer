"use client";

import { useEffect, useState } from "react";
import { Activity } from "lucide-react";
import Link from "next/link";
import ResultsView from "../../components/ResultsView";
import UploadForm from "../../components/UploadForm";

export default function Home() {
  const [apiStatus, setApiStatus] = useState("checking");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);
  const [jobTitle, setJobTitle] = useState("");

  useEffect(() => {
    const controller = new AbortController();

    fetch("/api/health", { cache: "no-store", signal: controller.signal })
      .then((response) => {
        if (!response.ok) throw new Error("API unavailable");
        return response.json();
      })
      .then(() => setApiStatus("connected"))
      .catch(() => {
        if (!controller.signal.aborted) setApiStatus("offline");
      });

    return () => controller.abort();
  }, []);

  async function analyzeResume(file, title, description) {
    setLoading(true);
    setError("");
    setJobTitle(title);

    const body = new FormData();
    body.append("resume_file", file);
    body.append("job_title", title);
    body.append("job_description_text", description);

    try {
      const response = await fetch("/api/analysis", { method: "POST", body });
      const data = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(data.detail || "The analysis could not be completed.");
      }
      setResult(data);
    } catch (requestError) {
      setError(requestError.message || "Could not reach the analysis service.");
    } finally {
      setLoading(false);
    }
  }

  function resetAnalysis() {
    setResult(null);
    setError("");
  }

  return (
    <div className="min-h-screen px-5 sm:px-8">
      <header className="mx-auto flex w-full max-w-6xl items-center justify-between border-b border-line py-5">
        <Link href="/" className="font-display text-sm font-bold tracking-wide text-ink">
          ROLE / READY
        </Link>
        <div
          className="flex items-center gap-2 text-sm text-slate"
          role="status"
          aria-live="polite"
        >
          <Activity size={16} aria-hidden />
          <span
            className={`h-2 w-2 rounded-full ${
              apiStatus === "connected"
                ? "bg-emerald-600"
                : apiStatus === "offline"
                  ? "bg-rose-600"
                  : "bg-amber-500"
            }`}
          />
          {apiStatus === "checking"
            ? "Checking API"
            : apiStatus === "connected"
              ? "API connected"
              : "API unavailable"}
        </div>
      </header>

      <main className="mx-auto w-full max-w-6xl pb-20 pt-12 sm:pt-16">
        <div className="max-w-3xl">
          <p className="mb-4 text-xs font-bold uppercase tracking-[0.14em] text-ultramarine">
            Resume and role alignment
          </p>
          <h1 className="font-display text-4xl font-semibold leading-tight text-ink sm:text-5xl">
            Make your next application count.
          </h1>
          <p className="mt-4 max-w-2xl text-base leading-7 text-slate sm:text-lg">
            Compare your resume with a role, see the skills that stand out, and focus your
            preparation where it matters.
          </p>
        </div>

        <div className="mt-10 border-t border-line pt-8 sm:mt-12 sm:pt-10">
          {result ? (
            <ResultsView result={result} jobTitle={jobTitle} onReset={resetAnalysis} />
          ) : (
            <UploadForm loading={loading} error={error} onSubmit={analyzeResume} />
          )}
        </div>
      </main>
    </div>
  );
}
