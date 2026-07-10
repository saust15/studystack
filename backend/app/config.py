from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    openai_api_key: str
    anthropic_api_key: str = ""
    database_url: str = "postgresql://studystack:studystack@localhost:5433/studystack"
    embedding_model: str = "text-embedding-3-small"
    chat_model: str = "gpt-4o-mini"          # LiteLLM model string; swap provider here
    ingest_api_key: str = "dev-only-change-me"  # protects POST /ingest


settings = Settings()
