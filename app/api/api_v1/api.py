from fastapi import APIRouter, Depends

from app.api.api_v1.endpoints import auth, users
from app.api.api_v1.endpoints import text_extraction, claimbuster, factcheck, llm_verify
from app.dependencies.auth import get_current_user

api_router = APIRouter()

# Public endpoints
api_router.include_router(auth.router)   # login/refresh (public)
api_router.include_router(users.router)  # register will be public; /me still protected

# Protected group for everything else
protected = APIRouter(dependencies=[Depends(get_current_user)])
protected.include_router(text_extraction.router)
protected.include_router(claimbuster.router)
protected.include_router(factcheck.router)
protected.include_router(llm_verify.router)

api_router.include_router(protected)
