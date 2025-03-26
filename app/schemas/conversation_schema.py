from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class CreateConversationSchema(BaseModel):
    user_id: str
    name: Optional[str] = None

class ConversationResponseSchema(BaseModel):
    id: str = Field(alias="_id")
    user_id: str
    name: Optional[str] = None
    created_at: Optional[str]

    class Config:
        json_encoders = {ObjectId: str}  # Đảm bảo ObjectId được chuyển thành string
        schema_extra = {
            "example": {
                "_id": "605c72f1e3b3c0c7a2f3c123",
                "user_id": "605c72f1e3b3c0c7a2f3c456",
                "name": "Chat với AI",
                "created_at": "2025-03-20T12:00:00"
            }
        }
