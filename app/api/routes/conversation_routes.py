from typing import List

from fastapi import APIRouter

from app.schemas.conversation_schema import CreateConversationSchema, ConversationResponseSchema
from app.services.conversation_service import ConversationService

conv_bp = APIRouter()

@conv_bp.post("/create", response_model=ConversationResponseSchema)
async def create_conversation(conv: CreateConversationSchema):
    return await ConversationService.create_conversation(conv)

@conv_bp.get("/all/{user_id}", response_model=List[ConversationResponseSchema])
async def get_conversations_by_user(user_id: str):
    return await ConversationService.get_conversations_by_user(user_id)

@conv_bp.get("/all}", response_model=List[ConversationResponseSchema])
async def get_conversations():
    return await ConversationService.get_conversations()