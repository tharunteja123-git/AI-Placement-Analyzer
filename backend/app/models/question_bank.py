import uuid
from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.config import settings
from app.database.session import Base


class QuestionBank(Base):
    """Curated interview questions, embedded for retrieval (this is the RAG corpus)."""

    __tablename__ = "question_bank"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    skill_tag: Mapped[str] = mapped_column(String(100), index=True)  # e.g. "react", "system-design"
    role_tag: Mapped[str] = mapped_column(String(100), index=True)  # e.g. "frontend", "ml-engineer"
    difficulty: Mapped[str] = mapped_column(String(20), default="mid")  # junior / mid / senior
    question: Mapped[str] = mapped_column(Text)
    embedding: Mapped[list[float]] = mapped_column(Vector(settings.embedding_dim))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
