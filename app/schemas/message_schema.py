from typing import Optional

from pydantic import BaseModel, Field


# Model khi tạo tin nhắn mới
class CreateMessageSchema(BaseModel):
    conversation_id: str
    question: str
    answer: str

class MessageResponseSchema(BaseModel):
    id: str = Field(alias="_id")
    conversation_id: str
    question: str
    answer: str
    created_at: Optional[str]
    update_at: Optional[str]

class UpdateMessageSchema(BaseModel):
    question: str | None = None
    answer: str | None = None
    update_at: Optional[str]