import json

from anthropic import AsyncAnthropic

from app.core.config import settings

_client = AsyncAnthropic(api_key=settings.anthropic_api_key)

SYSTEM_PROMPT = """You are an expert technical recruiter and career coach. You compare a
candidate's resume against a job description and produce a precise, honest gap analysis.

Respond with ONLY valid JSON (no markdown fences, no preamble) matching this shape:
{
  "match_score": <int 0-100>,
  "matched_skills": ["skill", ...],
  "missing_skills": ["skill", ...],
  "improvement_suggestions": [
    {"area": "skill or topic", "suggestion": "concrete, specific advice"},
    ...
  ]
}

Be specific and concrete. Do not pad the lists with vague or generic entries."""


async def run_gap_analysis(resume_text: str, job_description_text: str) -> dict:
    """Direct context-window comparison — no retrieval. Both documents are short
    enough to pass straight into the prompt, so RAG would add retrieval error
    risk without any benefit here."""
    message = await _client.messages.create(
        model=settings.claude_model,
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": (
                    f"RESUME:\n{resume_text}\n\n"
                    f"JOB DESCRIPTION:\n{job_description_text}\n\n"
                    "Produce the gap analysis JSON now."
                ),
            }
        ],
    )

    raw_text = "".join(block.text for block in message.content if block.type == "text")
    return json.loads(raw_text)
