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