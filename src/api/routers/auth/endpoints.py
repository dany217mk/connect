from datetime import timedelta

from fastapi import APIRouter, Depends, Security, HTTPException
from fastapi.responses import JSONResponse
from fastapi_jwt import JwtRefreshBearer, JwtAuthorizationCredentials, JwtAccessBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src import config
from src.api.routers.auth import models
from src.api.routers.auth.utils import get_hash_password, verify_password
from src.api.security import access_policy, refresh_policy
from src.api.sessions import get_db_session
from src.db import crud


router = APIRouter(
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.post("/register")
async def register(user: models.UserCreate, session: AsyncSession = Depends(get_db_session)):
    res = await crud.get_user_by_login(session, user.login)
    if res:
        return JSONResponse(
            status_code=400,
            content={"error": "Login already exists!"}
        )
    hashed_password = get_hash_password(user.password)
    res = await crud.add_user(session, user.login, user.name, hashed_password)
    subject = {"login": user.login, "name": user.name, "id": res.id}
    access_token = access_policy.create_access_token(subject=subject)
    refresh_token = refresh_policy.create_refresh_token(subject=subject)

    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/login")
async def login(user: models.UserLogin, session: AsyncSession = Depends(get_db_session)):
    res = await crud.get_user_by_login(session, user.login)
    if res:
        if verify_password(user.password, res.password):
            subject = {"login": res.login, "name": res.name, "id": res.id}
            access_token = access_policy.create_access_token(subject=subject)
            refresh_token = refresh_policy.create_refresh_token(subject=subject)
            return {"access_token": access_token, "refresh_token": refresh_token}
    return JSONResponse(
        status_code=401,
        content={"error": "Wrong login details!"}
    )


@router.post("/refresh")
def refresh(credentials: JwtAuthorizationCredentials = Security(refresh_policy)):
    access_token = access_policy.create_access_token(subject=credentials.subject)
    refresh_token = refresh_policy.create_refresh_token(subject=credentials.subject, expires_delta=timedelta(days=2))

    return {"access_token": access_token, "refresh_token": refresh_token}

@router.get("/test")
async def test(credentials: JwtAuthorizationCredentials = Security(access_policy)):
    return 'ok'
