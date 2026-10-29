from openai import AsyncOpenAI
from app.core.config import settings

_client= AsyncOpenAI(api_key=settings.openai_api_key)

async def embed_text(text:str)->list[float]:
    """Embed a single piece of text. Used both when indexing the question bank
    and when embedding a query (the gap/skill terms) at retrieval time."""
    response=await _client.embeddings.create(
        model=settings.embedding_model,
        input=text,
    )
    return response.data[0].embedding

async def embed_batch(texts:list[str])->list[list[float]]:
    """Batch embedding for indexing many question-bank entries at once."""
    response=await _client.embeddings.create(
        model=settings.embedding_model,
        input=texts,
    )
    return [item.embedding for item in response.data]