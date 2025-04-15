from fastapi import APIRouter, Header, HTTPException
from app.schemas.auth_schema import (
    RegisterSchema, 
    LoginSchema, 
    LoginResponseSchema, 
    ForgotPasswordSchema, 
    ForgotPasswordResponseSchema,
    VerifyOTPSchema,
    VerifyOTPResponseSchema,
    ResetPasswordSchema,
    ResetPasswordResponseSchema,
    GetAccountResponseSchema,
    ChangePasswordSchema,
    ChangePasswordResponseSchema
)
from app.services.auth_service import UserService

auth_bp = APIRouter()

@auth_bp.post("/register")
def register(request: RegisterSchema):
    return UserService.register(request)

@auth_bp.post("/login", response_model= LoginResponseSchema)
def login(request: LoginSchema):
    return UserService.login(request)

@auth_bp.post("/forgot-password", response_model=ForgotPasswordResponseSchema)
def forgot_password(request: ForgotPasswordSchema):
    return UserService.forgot_password(request)

@auth_bp.post("/verify-otp", response_model=VerifyOTPResponseSchema)
def verify_otp(request: VerifyOTPSchema):
    return UserService.verify_otp(request)

@auth_bp.post("/reset-password", response_model=ResetPasswordResponseSchema)
def reset_password(request: ResetPasswordSchema):
    return UserService.reset_password(request)

@auth_bp.get("/getAccount", response_model=GetAccountResponseSchema)
def get_account(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header is missing")
    return UserService.get_account(authorization)

@auth_bp.patch("/change-password", response_model=ChangePasswordResponseSchema)
def change_password(request: ChangePasswordSchema, authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header is missing")
    return UserService.change_password(request, authorization)