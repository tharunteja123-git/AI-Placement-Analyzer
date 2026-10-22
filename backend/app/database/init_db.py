import asyncio

from sqlalchemy import text
from app.database.session import Base, engine
from app.models.analysis import Analysis, InterviewQuestion, Resume, JobDescription
from app.models.question_bank import QuestionBank

async def init_db():
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.run_sync(Base.metadata.create_all)
    print("Database initialized: pgvector enabled, tables created.")


if __name__ == "__main__":
    asyncio.run(init_db())