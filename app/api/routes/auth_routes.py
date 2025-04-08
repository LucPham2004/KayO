from fastapi import APIRouter
from app.schemas.auth_schema import (
    RegisterSchema, 
    LoginSchema, 
    LoginResponseSchema, 
    ForgotPasswordSchema, 
    ForgotPasswordResponseSchema,
    VerifyOTPSchema,
    VerifyOTPResponseSchema,
    ResetPasswordSchema,
    ResetPasswordResponseSchema
)
from app.services.auth_service import UserService

auth_bp = APIRouter()

@auth_bp.post("/register")
def register(login: RegisterSchema):
    return UserService.register(login)

@auth_bp.post("/login", response_model= LoginResponseSchema)
def login(register: LoginSchema):
    return UserService.login(register)

@auth_bp.post("/forgot-password", response_model=ForgotPasswordResponseSchema)
def forgot_password(request: ForgotPasswordSchema):
    return UserService.forgot_password(request)

@auth_bp.post("/verify-otp", response_model=VerifyOTPResponseSchema)
def verify_otp(request: VerifyOTPSchema):
    return UserService.verify_otp(request)

@auth_bp.post("/reset-password", response_model=ResetPasswordResponseSchema)
def reset_password(request: ResetPasswordSchema):
    return UserService.reset_password(request)