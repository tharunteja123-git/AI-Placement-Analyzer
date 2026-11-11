"""Quick self-test for your Gemini setup.  Run from the backend folder:

    python -m app.check_gemini
"""
import asyncio

from app.core.config import settings
from app.services.llm import get_client
from app.services.rag.embeddings import embed_text


def list_models() -> None:
    print("\nModels your key can use for text generation:")
    for m in get_client().models.list():
        if "generateContent" in (m.supported_actions or []) and "flash" in m.name:
            print("  ", m.name.replace("models/", ""))
    print("Set GEMINI_MODEL in backend/.env to one of these names.")


async def main() -> None:
    print(f"Generation model: {settings.gemini_model}")
    print(f"Embedding model:  {settings.embedding_model} ({settings.embedding_dim} dims)")

    try:
        reply = await get_client().aio.models.generate_content(
            model=settings.gemini_model, contents="Reply with the single word: ready"
        )
        print("1. Generation works ->", (reply.text or "").strip())
    except Exception as e:  # noqa: BLE001 - this is a diagnostic script
        print("1. Generation FAILED ->", getattr(e, "message", None) or e)
        list_models()
        return

    try:
        vector = await embed_text("python developer")
        print(f"2. Embeddings work -> vector of {len(vector)} numbers")
        if len(vector) != settings.embedding_dim:
            print("   WARNING: size does not match EMBEDDING_DIM")
    except Exception as e:  # noqa: BLE001
        print("2. Embeddings FAILED ->", getattr(e, "detail", None) or e)
        return

    print("\nAll good. You can run: python -m app.database.seed_questions")


if __name__ == "__main__":
    asyncio.run(main())
