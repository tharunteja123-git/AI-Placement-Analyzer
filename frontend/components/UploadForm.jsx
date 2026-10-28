"use client";

import { useState } from "react";
import { Loader2 } from "lucide-react";
import Dropzone from "./Dropzone";

const MIN_JD_CHARS = 80;

export default function UploadForm({ loading, error, onSubmit }) {
  const [file, setFile] = useState(null);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  const ready = !!file && title.trim().length > 0 && description.trim().length >= MIN_JD_CHARS;
  const remaining = Math.max(0, MIN_JD_CHARS - description.trim().length);

  function handleSubmit(e) {
    e.preventDefault(); // stop the browser from reloading the page
    if (!file || !ready || loading) return;
    onSubmit(file, title.trim(), description.trim());
  }

  return (
    <form onSubmit={handleSubmit} className="mt-10">
      <div className="grid gap-8 lg:grid-cols-2">
        <section aria-labelledby="resume-heading">
          <h2 id="resume-heading" className="mb-3 font-display text-xl font-semibold">
            Your resume
          </h2>
          <Dropzone file={file} onChange={setFile} />
        </section>

        <section aria-labelledby="jd-heading">
          <h2 id="jd-heading" className="mb-3 font-display text-xl font-semibold">
            The job
          </h2>
          <label htmlFor="job-title" className="mb-1 block text-sm font-medium text-slate">
            Job title
          </label>
          <input
            id="job-title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Machine Learning Engineer"
            className="mb-4 w-full rounded-xl border border-line bg-white px-4 py-3 placeholder:text-slate/60 focus:border-ultramarine"
          />
          <label htmlFor="job-description" className="mb-1 block text-sm font-medium text-slate">
            Job description
          </label>
          <textarea
            id="job-description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={9}
            placeholder="Paste the full job posting, including responsibilities and requirements."
            className="w-full resize-y rounded-xl border border-line bg-white px-4 py-3 leading-relaxed placeholder:text-slate/60 focus:border-ultramarine"
          />
          {description.length > 0 && remaining > 0 && (
            <p className="mt-1 text-sm text-slate">
              Add a little more of the posting ({remaining} more characters) for a useful result.
            </p>
          )}
        </section>
      </div>

      {error && (
        <p
          role="alert"
          className="mt-6 rounded-xl border border-rose-ink/30 bg-rose/40 px-4 py-3 text-rose-ink"
        >
          {error}
        </p>
      )}

      <div className="mt-8 flex flex-wrap items-center gap-4">
        <button
          type="submit"
          disabled={!ready || loading}
          className="inline-flex items-center gap-2 rounded-xl bg-ultramarine px-6 py-3 font-semibold text-white transition-colors hover:bg-ultramarine-dark disabled:cursor-not-allowed disabled:bg-line disabled:text-slate"
        >
          {loading && <Loader2 size={18} className="animate-spin" aria-hidden />}
          {loading ? "Analyzing your resume" : "Analyze match"}
        </button>
        {loading && (
          <p className="text-sm text-slate" aria-live="polite">
            This usually takes 10 to 20 seconds.
          </p>
        )}
      </div>
    </form>
  );
}
