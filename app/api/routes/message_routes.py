from typing import List

from fastapi import APIRouter

from app.schemas.message_schema import MessageResponseSchema, CreateMessageSchema
from app.services.message_service import MessageService

message_bp = APIRouter()


@message_bp.post("/create", response_model=MessageResponseSchema)
def create_conversation(message: CreateMessageSchema):
    return MessageService.create_message(message)

@message_bp.get("/{message_id}", response_model=MessageResponseSchema)
def get_message_by_id(message_id: str):
    return MessageService.get_message_by_id(message_id)

@message_bp.get("/all/{conv_id}", response_model=List[MessageResponseSchema])
def get_messages(conv_id: str):
    return MessageService.get_messages(conv_id)

@message_bp.get("/history/{conv_id}", response_model=List[MessageResponseSchema])
def get_history(conv_id: str):
    return MessageService.get_history(conv_id)