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
    update_at: Optional[str]

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True

class UpdateConversationSchema(BaseModel):
    name: str | None = None
    update_at: Optional[str]