from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:pass@db:5432/nps"
    N_TOPICS: int = 5
    EMBED_MODEL: str = "paraphrase-multilingual-MiniLM-L12-v2"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()
