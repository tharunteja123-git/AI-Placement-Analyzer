from sqlalchemy.ext.asyncio import AsyncSession

from app.services.llm import generate_json
from app.services.rag.retriever import retrieve_for_gaps

SYSTEM_PROMPT = """You are an expert technical interviewer. You are given a candidate's
skill gaps and a set of retrieved, vetted interview questions for each gap. Personalize
and adapt these questions to the candidate's context rather than inventing new ones from
scratch. Stay close to the retrieved questions' intent and difficulty.
If no retrieved question exists for a gap, write one good question yourself.

Respond with ONLY valid JSON:
{
  "questions": [
    {"skill": "skill name", "question": "personalized question text"}
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

    context_lines = []
    for skill, questions in retrieved.items():
        context_lines.append(f"Skill gap: {skill}")
        for q in questions:
            context_lines.append(f"  - [{q.difficulty}] {q.question}")
    context_block = "\n".join(context_lines) if context_lines else "No matching questions found."

    result = await generate_json(
        SYSTEM_PROMPT,
        f"Candidate's skill gaps: {', '.join(missing_skills)}\n\n"
        f"Retrieved questions from the question bank:\n{context_block}\n\n"
        "Personalize one question per skill gap now.",
    )

    questions = []
    for item in result.get("questions", []) or []:
        if isinstance(item, dict) and item.get("question"):
            questions.append(
                {"skill": str(item.get("skill", "")), "question": str(item["question"])}
            )
    return {"questions": questions}
