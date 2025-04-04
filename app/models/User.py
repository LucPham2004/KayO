from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field

from app.models import PyObjectId


# Pydantic model cho User (dùng khi trả về response)
class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    username: str
    email: EmailStr
    password: str
    avatar_url: Optional[str] = None
    created_at: Optional[str]
    update_at: Optional[str]

    class Config:
        json_encoders = {ObjectId: str}


