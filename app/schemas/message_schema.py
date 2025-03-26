from typing import Optional

from pydantic import BaseModel, Field

from app.models.User import PyObjectId


# Model khi tạo tin nhắn mới
class CreateMessageModel(BaseModel):
    conversation_id: PyObjectId
    question: str
    answer: str

class MessageResponse(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    conversation_id: PyObjectId
    question: str
    answer: str
    created_at: Optional[str]