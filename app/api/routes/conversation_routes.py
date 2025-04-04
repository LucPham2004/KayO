from typing import List

from fastapi import APIRouter

from app.schemas.conversation_schema import CreateConversationSchema, ConversationResponseSchema, \
    UpdateConversationSchema
from app.services.conversation_service import ConversationService

conv_bp = APIRouter()

@conv_bp.post("/create", response_model=ConversationResponseSchema)
def create_conversation(conv: CreateConversationSchema):
    return ConversationService.create_conversation(conv)

@conv_bp.get("/all/{user_id}", response_model=List[ConversationResponseSchema])
def get_conversations_by_user(user_id: str):
    return ConversationService.get_conversations_by_user(user_id)

@conv_bp.get("/all", response_model=List[ConversationResponseSchema])
def get_conversations():
    return ConversationService.get_conversations()

@conv_bp.put("/{id}", response_model=ConversationResponseSchema)
def update_conversation(id: str, update_data: UpdateConversationSchema):
    return ConversationService.update_conversation(id, update_data.model_dump(exclude_unset=True))

@conv_bp.delete("/{id}")
def delete_conversation(id: str):
    return ConversationService.delete_conversation(id)