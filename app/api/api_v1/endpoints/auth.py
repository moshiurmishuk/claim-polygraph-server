from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import verify_password, create_access_token, create_refresh_token
from app.db.session import get_db
from app.services.user_service import get_user_by_email
from app.schemas.auth import TokenResponse
from app.dependencies.auth import get_refresh_subject, get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=TokenResponse)
def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = get_user_by_email(db, form_data.username)  # username = email
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(subject=user.email)
    refresh_token = create_refresh_token(subject=user.email)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        path="/",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600,
    )

    return TokenResponse(access_token=access_token)

@router.post("/refresh", response_model=TokenResponse)
def refresh(subject: str = Depends(get_refresh_subject)):
    return TokenResponse(access_token=create_access_token(subject=subject))

# Logout should be protected (only logged-in users can call it)
@router.post("/logout")
def logout(response: Response, _user=Depends(get_current_user)):
    response.delete_cookie(key="refresh_token", path="/")
    return {"status": "ok"}
