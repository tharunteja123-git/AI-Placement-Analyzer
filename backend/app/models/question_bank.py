import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, Text, func,Base
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

class QuestionBank(Base):
    __tablename__ = "question_bank"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    skill_tag: Mapped[str] = mapped_column(String(100),index=True)
    role_tag:Mapped[str]=mapped_column(String(100),index=True)
    difficulty:Mapped[str]=mapped_column(String(20),default="mid")
    question: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    