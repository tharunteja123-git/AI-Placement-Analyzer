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


import math

from fastapi import HTTPException
from google.genai import errors, types

from app.core.config import settings
from app.services.llm import get_client, to_http_error



def _normalize(vector: list[float]) -> list[float]:
    norm = math.sqrt(sum(x * x for x in vector)) or 1.0
    return [x / norm for x in vector]


async def _embed(texts: list[str], task_type: str) -> list[list[float]]:
    results: list[list[float]] = []
    for i in range(0, len(texts), BATCH_SIZE):
        chunk = texts[i : i + BATCH_SIZE]
        try:
            response = await get_client().aio.models.embed_content(
                model=settings.embedding_model,
                contents=chunk,
                config=types.EmbedContentConfig(
                    task_type=task_type,
                    output_dimensionality=settings.embedding_dim,
                ),
            )
        except errors.APIError as e:
            raise to_http_error(e) from e
        if not response.embeddings or len(response.embeddings) != len(chunk):
            raise HTTPException(502, "Gemini returned an unexpected embeddings response.")
        results.extend(_normalize(list(e.values)) for e in response.embeddings)
    return results


async def embed_text(text: str) -> list[float]:
    """Embed a search query (used by the retriever)."""
    return (await _embed([text], "RETRIEVAL_QUERY"))[0]


async def embed_batch(texts: list[str]) -> list[list[float]]:
    """Embed documents for storage (used by the seed script)."""
    return await _embed(texts, "RETRIEVAL_DOCUMENT")