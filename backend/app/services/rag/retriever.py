from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.question_bank import QuestionBank
from app.services.rag.embeddings import embed_text


async def retrieve_questions(
    db: AsyncSession,
    skill: str,
    role: str | None = None,
    top_k: int = 3,
) -> list[QuestionBank]:
    """Retrieve the top-k most relevant curated questions for a given skill gap.

    This is the 'R' in RAG: instead of asking the LLM to invent questions from
    scratch, we pull real, vetted questions from the vector store and only ask
    the LLM to adapt/personalize them to the candidate's resume.
    """
    query_vector = await embed_text(f"{skill} interview question" + (f" for {role}" if role else ""))

    stmt = select(QuestionBank).order_by(QuestionBank.embedding.cosine_distance(query_vector))

    if role:
        stmt = stmt.where(QuestionBank.role_tag == role)

    stmt = stmt.limit(top_k)

    result = await db.execute(stmt)
    return list(result.scalars().all())


async def retrieve_for_gaps(
    db: AsyncSession,
    missing_skills: list[str],
    role: str | None = None,
    top_k_per_skill: int = 2,
) -> dict[str, list[QuestionBank]]:
    """Retrieve questions for every missing skill found in the gap analysis."""
    results: dict[str, list[QuestionBank]] = {}
    for skill in missing_skills:
        results[skill] = await retrieve_questions(db, skill, role, top_k_per_skill)
    return results
