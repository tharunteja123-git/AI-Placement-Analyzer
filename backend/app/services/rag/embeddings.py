import math

from fastapi import HTTPException
from google.genai import errors, types

from app.core.config import settings
from app.services.llm import get_client, to_http_error

BATCH_SIZE = 100  # Gemini accepts up to 100 texts per embedding request


def _normalize(vector: list[float]) -> list[float]:
    # Gemini only pre-normalizes the full-size vector, so we normalize the
    # shortened (768-dim) version ourselves.
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
