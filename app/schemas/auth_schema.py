from pydantic import BaseModel, Field

class RegisterSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    confirmPassword: str = Field(..., min_length=6)

class LoginSchema(BaseModel):
    username: str
    password: str