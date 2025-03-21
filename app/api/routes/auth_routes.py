from fastapi import APIRouter
from app.schemas.auth_schema import RegisterSchema, LoginSchema
from app.services.auth_service import UserService

auth_bp = APIRouter()

@auth_bp.post("/register")
def register(user_data: RegisterSchema):
    return UserService.register(user_data.username, user_data.password)

@auth_bp.post("/login")
def login(user_data: LoginSchema):
    return UserService.login(user_data.username, user_data.password)