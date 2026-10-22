import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.analysis import Analysis, InterviewQuestion
from app.models.schemas import InterviewQuestionsResponse
from app.services.interview_questions import generate_interview_questions

router = APIRouter(prefix="/api/interview-questions", tags=["interview-questions"])


@router.post("/{analysis_id}", response_model=InterviewQuestionsResponse)
async def generate_questions(analysis_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    analysis = await db.get(Analysis, analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    if not analysis.missing_skills:
        return InterviewQuestionsResponse(analysis_id=analysis.id, questions=[])

    result = await generate_interview_questions(db, analysis.missing_skills)

    question_rows = [
        InterviewQuestion(analysis_id=analysis.id, skill_tag=item["skill"], question=item["question"])
        for item in result["questions"]
    ]
    db.add_all(question_rows)
    await db.commit()

    return InterviewQuestionsResponse(analysis_id=analysis.id, questions=result["questions"])


@router.get("/{analysis_id}", response_model=InterviewQuestionsResponse)
async def get_questions(analysis_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    stmt = select(InterviewQuestion).where(InterviewQuestion.analysis_id == analysis_id)
    result = await db.execute(stmt)
    rows = result.scalars().all()
    return InterviewQuestionsResponse(
        analysis_id=analysis_id,
        questions=[{"skill": r.skill_tag, "question": r.question} for r in rows],
    )
