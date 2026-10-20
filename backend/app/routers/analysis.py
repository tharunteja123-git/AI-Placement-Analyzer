from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.models.analysis import Analysis, JobDescription, Resume
from app.models.schemas import GapAnalysisResponse
from pdfminer.high_level import extract_text





router = APIRouter(prefix="/api/analysis", tags=["analysis"])


@router.post("", response_model=GapAnalysisResponse)
async def analyze(
    resume_file: UploadFile,
    job_title: str = Form(...),
    job_description_text: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    try:
        resume_text = await extract_text(resume_file)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not resume_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from resume")

    resume = Resume(filename=resume_file.filename, raw_text=resume_text)
    job_description = JobDescription(title=job_title, raw_text=job_description_text)
    db.add_all([resume, job_description])
    await db.flush()

    result = await run_gap_analysis(resume_text, job_description_text)

    analysis = Analysis(
        resume_id=resume.id,
        job_description_id=job_description.id,
        matched_skills=result["matched_skills"],
        missing_skills=result["missing_skills"],
        improvement_suggestions=result["improvement_suggestions"],
        match_score=result["match_score"],
    )
    db.add(analysis)
    await db.commit()
    await db.refresh(analysis)

    return GapAnalysisResponse(
        analysis_id=analysis.id,
        match_score=analysis.match_score,
        matched_skills=analysis.matched_skills,
        missing_skills=analysis.missing_skills,
        improvement_suggestions=analysis.improvement_suggestions,
    )
