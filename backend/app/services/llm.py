
import json
from functools import lru_cache

from fastapi import HTTPException
from google import genai
from google.genai import errors, types

from app.core.config import settings


@lru_cache
def get_client() -> genai.Client:
    if not settings.gemini_api_key.strip():
        raise HTTPException(
            status_code=500,
            detail="GEMINI_API_KEY is not set. Add it to backend/.env and restart the server.",
        )
    return genai.Client(api_key=settings.gemini_api_key.strip())


def to_http_error(e: errors.APIError) -> HTTPException:
    code = getattr(e, "code", None)
    msg = getattr(e, "message", None) or str(e)
    if code == 429:
        return HTTPException(
            429, "Gemini free-tier limit reached. Wait a minute and try again."
        )
    if code in (401, 403) or (code == 400 and "API key" in msg):
        return HTTPException(
            502, "Gemini rejected the API key. Check GEMINI_API_KEY in backend/.env."
        )
    if code == 404:
        return HTTPException(
            502,
            f"Gemini model '{settings.gemini_model}' was not found. "
            "Run: python -m app.check_gemini to list available models.",
        )
    return HTTPException(502, f"Gemini request failed ({code}): {msg}")


def parse_json(text: str) -> dict:
    """Parse JSON even if the model wrapped it in code fences or added extra words."""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else cleaned
        cleaned = cleaned.rsplit("```", 1)[0]
    start, end = cleaned.find("{"), cleaned.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("no JSON object found")
    return json.loads(cleaned[start : end + 1])


async def generate_json(system: str, user: str) -> dict:
    """Ask Gemini a question and get back a Python dict."""
    try:
        response = await get_client().aio.models.generate_content(
            model=settings.gemini_model,
            contents=user,
            config=types.GenerateContentConfig(
                system_instruction=system,
                response_mime_type="application/json",
                temperature=0.3,
                max_output_tokens=8192,
            ),
        )
    except errors.APIError as e:
        raise to_http_error(e) from e

    text = response.text
    if not text:
        raise HTTPException(
            502, "Gemini returned an empty reply (it may have been blocked). Try again."
        )
    try:
        return parse_json(text)
    except ValueError as e:  
        raise HTTPException(
            502, "Gemini returned a reply that was not valid JSON. Try again."
        ) from e
