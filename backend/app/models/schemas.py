import uuid
from pydantic import BaseModel

class ImprovementSuggestion(BaseModel):
    skill: str
    suggestion: str

class GapAnalysisResponse(BaseModel):
    analysis_id:uuid.UUID
    match_score:int
    matched_skills:list[str]
    missing_skills:list[str]
    improvement_suggestions:list[ImprovementSuggestion]

class InterviewQuestionItem(BaseModel):
    skill:str
    question:str

class InterviewQuestionsResponse(BaseModel):
    analysis_id:uuid.UUID
    interview_questions:list[InterviewQuestionItem]

class AnalysisRequest(BaseModel):
    job_title:str
    job_description_text:str