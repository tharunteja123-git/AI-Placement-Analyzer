import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base


class Resume(Base):
    __tablename__ = "resumes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename: Mapped[str] = mapped_column(String(255))
    raw_text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    analyses: Mapped[list["Analysis"]] = relationship(back_populates="resume")


class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255))
    raw_text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    analyses: Mapped[list["Analysis"]] = relationship(back_populates="job_description")


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resume_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("resumes.id"))
    job_description_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("job_descriptions.id"))
    matched_skills: Mapped[list[str]] = mapped_column(JSONB, default=list)
    missing_skills: Mapped[list[str]] = mapped_column(JSONB, default=list)
    improvement_suggestions: Mapped[list[dict[str, str]]] = mapped_column(JSONB, default=list)
    match_score: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    resume: Mapped[Resume] = relationship(back_populates="analyses")
    job_description: Mapped[JobDescription] = relationship(back_populates="analyses")
    interview_questions: Mapped[list["InterviewQuestion"]] = relationship(back_populates="analysis")


class InterviewQuestion(Base):
    __tablename__ = "interview_questions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    analysis_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("analyses.id"))
    skill_tag: Mapped[str] = mapped_column(String(100))
    question: Mapped[str] = mapped_column(Text)
    source_bank_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("question_bank.id"), nullable=True)

    analysis: Mapped[Analysis] = relationship(back_populates="interview_questions")
