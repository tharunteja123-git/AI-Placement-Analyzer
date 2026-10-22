import asyncio

from app.database.session import AsyncSessionLocal
from app.models.question_bank import QuestionBank
from app.services.rag.embeddings import embed_batch

SEED_QUESTIONS = [
      {"skill_tag": "react", "role_tag": "frontend", "difficulty": "mid",
     "question": "Walk me through how you'd optimize a React component that re-renders too often."},
    {"skill_tag": "react", "role_tag": "frontend", "difficulty": "senior",
     "question": "How would you design state management for a large React app without Redux?"},
    {"skill_tag": "system-design", "role_tag": "backend", "difficulty": "senior",
     "question": "Design a URL shortener that handles 100M requests/day. Walk through your approach."},
    {"skill_tag": "sql", "role_tag": "backend", "difficulty": "mid",
     "question": "Explain the difference between a LEFT JOIN and an INNER JOIN with an example."},
    {"skill_tag": "python", "role_tag": "backend", "difficulty": "mid",
     "question": "What's the difference between a list and a generator in Python, and when would you use each?"},
    {"skill_tag": "machine-learning", "role_tag": "ml-engineer", "difficulty": "mid",
     "question": "How would you detect and handle overfitting in a model you're training?"},
    {"skill_tag": "vector-databases", "role_tag": "ml-engineer", "difficulty": "mid",
     "question": "Explain how approximate nearest neighbor search works and why it's used in vector databases."},
    {"skill_tag": "docker", "role_tag": "devops", "difficulty": "junior",
     "question": "What's the difference between a Docker image and a Docker container?"},
    {"skill_tag": "aws", "role_tag": "devops", "difficulty": "mid",
     "question": "How would you design a highly available architecture on AWS for a web application?"},
    {"skill_tag": "typescript", "role_tag": "frontend", "difficulty": "mid",
     "question": "When would you use a TypeScript interface versus a type alias?"},
]

async def seed():
    texts = [q["question"] for q in SEED_QUESTIONS]
    embeddings = await embed_batch(texts)

    async with AsyncSessionLocal() as db:
        for q, emb in zip(SEED_QUESTIONS, embeddings):
            db.add(QuestionBank(**q, embedding=emb))
        await db.commit()

    print(f"Seeded {len(SEED_QUESTIONS)} questions into question_bank.")


if __name__ == "__main__":
    asyncio.run(seed())

