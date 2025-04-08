from pydantic import BaseModel, Field, model_validator, EmailStr
from typing import Optional


class RegisterSchema(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    confirmPassword: str = Field(..., min_length=6)

    @model_validator(mode='after')
    def check_passwords_match(self):
        if self.password != self.confirmPassword:
            raise ValueError('Passwords do not match')
        return self

class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserSchema(BaseModel):
    _id: str
    email: str
    username: str

class LoginResponseSchema(BaseModel):
    message: str
    user: UserSchema
    access_token: str

class ForgotPasswordSchema(BaseModel):
    email: EmailStr

class ForgotPasswordResponseSchema(BaseModel):
    message: str

class VerifyOTPSchema(BaseModel):
    email: EmailStr
    otp: str

class VerifyOTPResponseSchema(BaseModel):
    message: str
    is_valid: bool

class ResetPasswordSchema(BaseModel):
    email: EmailStr
    otp: str
    newPassword: str = Field(..., min_length=6)
    confirmPassword: str = Field(..., min_length=6)

    @model_validator(mode='after')
    def check_passwords_match(self):
        if self.newPassword != self.confirmPassword:
            raise ValueError('Mật khẩu không khớp')
        return self

class ResetPasswordResponseSchema(BaseModel):
    message: str