from typing import List

from fastapi import APIRouter

from app.schemas.message_schema import MessageResponseSchema, CreateMessageSchema
from app.services.message_service import MessageService

message_bp = APIRouter()


@message_bp.post("/create", response_model=MessageResponseSchema)
async def create_conversation(message: CreateMessageSchema):
    return await MessageService.create_message(message)

@message_bp.get("/{message_id}", response_model=MessageResponseSchema)
async def get_message_by_id(message_id: str):
    return await MessageService.get_message_by_id(message_id)

@message_bp.get("/all/{conv_id}", response_model=List[MessageResponseSchema])
async def get_messages(conv_id: str):
    return await MessageService.get_messages(conv_id)

@message_bp.get("/history/{conv_id}", response_model=List[MessageResponseSchema])
async def get_history(conv_id: str):
    return await MessageService.get_history(conv_id)