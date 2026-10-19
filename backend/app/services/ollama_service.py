import httpx

from app.core.config import settings


async def embed(text: str) -> list[float]:

    async with httpx.AsyncClient(
        timeout=120
    ) as client:

        response = await client.post(

            f"{settings.ollama_url}/api/embed",

            json={
                "model": settings.ollama_embed_model,
                "input": text
            }
        )

        response.raise_for_status()

        return response.json()["embeddings"][0]


async def generate(prompt: str) -> str:

    async with httpx.AsyncClient(
        timeout=300
    ) as client:

        response = await client.post(

            f"{settings.ollama_url}/api/generate",

            json={
                "model": settings.ollama_llm_model,
                "prompt": prompt,
                "stream": False
            }
        )

        response.raise_for_status()

        return response.json()["response"]