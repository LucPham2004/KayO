from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from app.models.User import PyObjectId


class ConversationModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    user_id: PyObjectId
    messages: List[PyObjectId]
    name: Optional[str] = None
    created_at: Optional[str]

    class Config:
        json_encoders = {ObjectId: str}

# Model khi tạo cuộc trò chuyện mới
class CreateConversationModel(BaseModel):
    messages: List[PyObjectId]
    name: Optional[str] = None
