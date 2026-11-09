from app.services.llm import generate_json

SYSTEM_PROMPT = """You are an expert technical recruiter and career coach. You compare a
candidate's resume against a job description and produce a precise, honest gap analysis.

Respond with ONLY valid JSON matching this shape:
{
  "match_score": <int 0-100>,
  "matched_skills": ["skill", ...],
  "missing_skills": ["skill", ...],
  "improvement_suggestions": [
    {"area": "skill or topic", "suggestion": "concrete, specific advice"}
  ]
}

Be specific and concrete. Do not pad the lists with vague or generic entries."""


def _string_list(value) -> list[str]:
    return [str(x) for x in value] if isinstance(value, list) else []


async def run_gap_analysis(resume_text: str, job_description_text: str) -> dict:
    """Direct context-window comparison: no retrieval. Both documents are short
    enough to pass straight into the prompt."""
    result = await generate_json(
        SYSTEM_PROMPT,
        f"RESUME:\n{resume_text}\n\nJOB DESCRIPTION:\n{job_description_text}\n\n"
        "Produce the gap analysis JSON now.",
    )

    # Normalize so a slightly-off reply can't cause a KeyError later
    try:
        score = max(0, min(100, int(result.get("match_score", 0))))
    except (TypeError, ValueError):
        score = 0

    suggestions = []
    for item in result.get("improvement_suggestions", []) or []:
        if isinstance(item, dict):
            suggestions.append(
                {
                    "area": str(item.get("area", "")),
                    "suggestion": str(item.get("suggestion", "")),
                }
            )

    return {
        "match_score": score,
        "matched_skills": _string_list(result.get("matched_skills")),
        "missing_skills": _string_list(result.get("missing_skills")),
        "improvement_suggestions": suggestions,
    }
