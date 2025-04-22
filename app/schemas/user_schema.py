from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


# Model khi tạo user mới
class CreateUserSchema(BaseModel):
    username: str
    email: str
    avatar_url: Optional[str] = None

class UserResponseSchema(BaseModel):
    id: str = Field(alias="_id")
    username: str
    email: str
    role: Optional[str]
    avatar_url: Optional[str] = None
    created_at: Optional[str]
    update_at: Optional[str] = None

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True
        json_schema_extra = {"example": {"id": "67efef29f0c4127199dd6fb5"}}


class UpdateUserSchema(BaseModel):
    email: str | None = None
    avatar_url: str | None = None
    update_at: Optional[str]