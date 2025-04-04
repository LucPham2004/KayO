from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from app.models import PyObjectId


class ConversationModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    user_id: PyObjectId
    messages: List[PyObjectId]
    name: Optional[str] = None
    created_at: Optional[str]
    update_at: Optional[str]

    class Config:
        json_encoders = {ObjectId: str}