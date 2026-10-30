"use client";

import { RotateCcw } from "lucide-react";
import ScoreRing, { scoreVerdict } from "./ScoreRing";
import SkillMarker from "./SkillMarker";
import QuestionsPanel from "./QuestionsPanel";

// Props: result (the object returned by analyze()), jobTitle (string), onReset()
export default function ResultsView({ result, jobTitle, onReset }) {
  const { matched_skills, missing_skills, improvement_suggestions } = result;

  return (
    <div className="mt-10 space-y-12">
      <div className="flex flex-wrap items-center gap-8">
        <ScoreRing score={result.match_score} />
        <div className="min-w-0 flex-1">
          <p className="text-slate">Your resume against</p>
          <h2 className="font-display text-3xl font-bold leading-tight sm:text-4xl">{jobTitle}</h2>
          <p className="mt-2 text-lg">{scoreVerdict(result.match_score)}</p>
          <button
            type="button"
            onClick={onReset}
            className="mt-4 inline-flex items-center gap-2 rounded-lg py-1 text-sm font-medium text-ultramarine hover:text-ultramarine-dark"
          >
            <RotateCcw size={16} aria-hidden />
            Analyze another resume
          </button>
        </div>
      </div>

      <div className="grid gap-10 md:grid-cols-2">
        <section aria-labelledby="have-heading">
          <h3 id="have-heading" className="font-display text-xl font-semibold">
            Skills you already show
          </h3>
          {matched_skills.length === 0 ? (
            <p className="mt-3 text-slate">No skills from the posting were found on your resume.</p>
          ) : (
            <ul className="mt-4 flex flex-wrap gap-x-2 gap-y-3">
              {matched_skills.map((s, i) => (
                <SkillMarker key={s} skill={s} kind="matched" index={i} />
              ))}
            </ul>
          )}
        </section>

        <section aria-labelledby="gap-heading">
          <h3 id="gap-heading" className="font-display text-xl font-semibold">
            Skills to build
          </h3>
          {missing_skills.length === 0 ? (
            <p className="mt-3 text-slate">Your resume covers everything the posting asks for.</p>
          ) : (
            <ul className="mt-4 flex flex-wrap gap-x-2 gap-y-3">
              {missing_skills.map((s, i) => (
                <SkillMarker key={s} skill={s} kind="missing" index={i + matched_skills.length} />
              ))}
            </ul>
          )}
        </section>
      </div>

      {improvement_suggestions.length > 0 && (
        <section aria-labelledby="improve-heading">
          <h3 id="improve-heading" className="font-display text-2xl font-semibold">
            What to improve
          </h3>
          <ul className="mt-5 space-y-5">
            {improvement_suggestions.map((item, i) => (
              <li key={`${item.area}-${i}`} className="border-l-4 border-ultramarine pl-5">
                <p className="font-display text-lg font-semibold">{item.area}</p>
                <p className="mt-1 max-w-2xl leading-relaxed text-slate">{item.suggestion}</p>
              </li>
            ))}
          </ul>
        </section>
      )}

      <QuestionsPanel analysisId={result.analysis_id} hasGaps={missing_skills.length > 0} />
    </div>
  );
}