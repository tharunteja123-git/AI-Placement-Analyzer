from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers.analysis import router as analysis_router
from app.routers.interview_questions import router as interview_questions_router

app = FastAPI(title="AI PLACEMENT ANALYZER", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin for origin in settings.cors_origin_list if origin]
    or ["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis_router)
app.include_router(interview_questions_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/")
def root():
    return {"message": "Hello FastAPI, AI Placement Analyzer is live!"}