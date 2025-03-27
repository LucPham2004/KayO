from fastapi import APIRouter
from app.schemas.auth_schema import RegisterSchema, LoginSchema, LoginResponseSchema
from app.services.auth_service import UserService

auth_bp = APIRouter()

@auth_bp.post("/register")
def register(login: RegisterSchema):
    return UserService.register(login)

@auth_bp.post("/login", response_model= LoginResponseSchema)
def login(register: LoginSchema):
    return UserService.login(register)