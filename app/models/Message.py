from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from app.models import PyObjectId


class MessageModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    conversation_id: PyObjectId
    question: str
    answer: str
    created_at: Optional[str]

    class Config:
        json_encoders = {ObjectId: str}
