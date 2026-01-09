from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="ignore")

    APP_NAME: str = "Claim-Polygraph API"
    DEBUG: bool = False

    # CORS (React dev servers)
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # DB (use sqlite for now; switch to Postgres later)
    DATABASE_URL: str = "sqlite:///./dev.db"

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 14

    # Cookie for refresh token
    COOKIE_SECURE: bool = False       # True in production (HTTPS)
    COOKIE_SAMESITE: str = "lax"      # if React is on a different domain + HTTPS use "none"


    # ClaimBuster
    CLAIMBUSTER_API_KEY: str
    CLAIMBUSTER_BATCH_URL: str = "https://idir.uta.edu/claimbuster/api/v2/score/text/sentences/"
    CLAIMBUSTER_TIMEOUT_SECONDS: int = 30

    # Google Fact Checking
    FACT_CHECK_API_KEY: str
    FACTCHECK_ENDPOINT: str = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
    FACTCHECK_TIMEOUT_SECONDS: int = 30

    # OpenAI / LLM
    OPENAI_API_KEY: str

    # LLM tuning
    LLM_TOP_N_CLAIMS: int = 3
    LLM_MIN_SOURCES: int = 2


settings = Settings()
