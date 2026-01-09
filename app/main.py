from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import configure_logging
from app.api.api_v1.api import api_router

from app.db.session import engine
from app.db.base import Base
from app.models import user  # noqa: F401  (ensures model is registered)

def create_app() -> FastAPI:
    configure_logging()

    app = FastAPI(
        title=settings.APP_NAME,
        debug=getattr(settings, "DEBUG", False),
        version="1.0.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=getattr(settings, "CORS_ORIGINS", ["http://localhost:3000", "http://localhost:5173"]),
        allow_credentials=True,  # IMPORTANT for refresh cookie
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix="/api/v1")

    @app.get("/health", tags=["health"])
    def health():
        return {"status": "ok"}

    return app

app = create_app()

# dev convenience (SQLite). For real prod use Alembic migrations.
Base.metadata.create_all(bind=engine)
