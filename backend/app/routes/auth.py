from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str


@router.post("/auth/login")
async def login(payload: LoginRequest):
    # TODO: implement real auth
    return {"access_token": "dev-token", "token_type": "bearer"}


@router.post("/auth/register")
async def register(payload: RegisterRequest):
    # TODO: persist user
    return {"status": "registered"}
