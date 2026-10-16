import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import UUID,JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Resume(Base):
    __tablename__ = "resumes"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resume_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("resumes.id"))
    job_description_id:Mapped[uuid.UUID] = mapped_column(ForeignKey("job_descriptions.id"))

    matched_skills:Mapped[list]=mapped_column(JSONB,default=list)
    missing_skills:Mapped[list]=mapped_column(JSONB,default=list)
    improvement_suggestions:Mapped[list]=mapped_column(JSONB,default=list)
    match_score:Mapped[int]=mapped_column(default=0)

    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True), server_default=func.now())
    resume: Mapped["Resume"] = relationship("Resume", back_populates="analyses")
    job_description:Mapped["JobDescription"]=relationship(back_populates="analyses")
    interview_questions:Mapped[list["InterviewQuestion"]]=relationship(back_populates="analysis")


class InterviewQuestion(Base):
    __tablename__ = "interview_questions"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    analysis_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("analyses.id"))
    skill_tag: Mapped[str] = mapped_column(String(100))
    question:Mapped[str]=mapped_column(Text)
    source_bank_id:Mapped[uuid.UUID | None] = mapped_column(ForeignKey("question_banks.id"), nullable=True)

    analysis:Mapped["Analysis"]=relationship(back_populates="interview_questions")


   
