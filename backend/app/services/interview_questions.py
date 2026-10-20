import json

from anthropic import AsyncAnthropic
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings


_client = AsyncAnthropic(api_key=settings.anthropic_api_key)

SYSTEM_PROMPT = """You are an expert technical interviewer. You are given a candidate's
skill gaps and a set of retrieved, vetted interview questions for each gap. Personalize
and adapt these questions to the candidate's context rather than inventing new ones from
scratch — stay close to the retrieved questions' intent and difficulty.

Respond with ONLY valid JSON (no markdown fences):
{
  "questions": [
    {"skill": "skill name", "question": "personalized question text"},
    ...
  ]
}"""


async def generate_interview_questions(
    db: AsyncSession,
    missing_skills: list[str],
    role: str | None = None,
) -> dict:
    """RAG flow: retrieve curated questions per skill gap from the vector store,
    then ask the LLM to personalize/adapt them rather than generate from nothing."""
    retrieved = await retrieve_for_gaps(db, missing_skills, role)

    # Build the retrieved context block the LLM will ground its answer in
    context_lines = []
    for skill, questions in retrieved.items():
        context_lines.append(f"Skill gap: {skill}")
        for q in questions:
            context_lines.append(f"  - [{q.difficulty}] {q.question}")
    context_block = "\n".join(context_lines) if context_lines else "No matching questions found in bank."

    message = await _client.messages.create(
        model=settings.claude_model,
        max_tokens=1500,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Candidate's skill gaps: {', '.join(missing_skills)}\n\n"
                    f"Retrieved questions from the question bank:\n{context_block}\n\n"
                    "Personalize one question per skill gap now."
                ),
            }
        ],
    )

    raw_text = "".join(block.text for block in message.content if block.type == "text")
    return json.loads(raw_text)
