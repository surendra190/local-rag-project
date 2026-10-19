
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# Project root:
# C:\local-rag-project
BASE_DIR = Path(__file__).resolve().parents[3]

ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):

    app_name: str = "Local RAG API"

    database_url: str

    s3_endpoint_url: str = "http://localhost:4566"
    s3_bucket: str = "documents"

    aws_access_key_id: str = "test"
    aws_secret_access_key: str = "test"
    aws_region: str = "us-east-1"

    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "documents"

    ollama_url: str = "http://localhost:11434"
    ollama_llm_model: str = "qwen2.5:3b"
    ollama_embed_model: str = "nomic-embed-text"

    top_k: int = 5

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        extra="ignore"
    )


settings = Settings()

