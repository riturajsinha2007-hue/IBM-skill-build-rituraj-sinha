"""
Application configuration – reads from .env / environment variables.
"""
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # IBM watsonx.ai
    watsonx_api_key: str = ""
    watsonx_project_id: str = ""
    watsonx_url: str = "https://us-south.ml.cloud.ibm.com"

    # Granite model IDs
    granite_chat_model: str = "ibm/granite-13b-chat-v2"
    granite_instruct_model: str = "ibm/granite-13b-instruct-v2"

    # Vector DB
    vector_db: str = "chroma"
    chroma_persist_dir: str = "./data/chroma_db"

    # App
    cors_origin: str = "http://localhost:3000"
    log_level: str = "INFO"
    max_conversation_history: int = 20

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
