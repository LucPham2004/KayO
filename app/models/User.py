from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field


# Helper để chuyển ObjectId sang string
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)


# Pydantic model cho User (dùng khi trả về response)
class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    username: str
    email: EmailStr
    avatar_url: Optional[str] = None
    created_at: Optional[str]

    class Config:
        json_encoders = {ObjectId: str}


# Model khi tạo user mới
class CreateUserModel(BaseModel):
    username: str
    email: EmailStr
    avatar_url: Optional[str] = None
