from datetime import datetime

from fastapi import HTTPException
from pymongo.collection import Collection

from app.config.database import MongoDB
from app.schemas.message_schema import CreateMessageSchema


class MessageService:
    @staticmethod
    async def create_message(message: CreateMessageSchema):
        db = MongoDB.get_db()
        messages: Collection = db["messages"]

        message_dict = message.model_dump()
        message_dict["created_at"] = datetime.now().isoformat()

        result = messages.insert_one(message_dict)
        new_message = await messages.find_one({"_id": result.inserted_id})

        if new_message:
            new_message["_id"] = str(new_message["_id"])

        return new_message

    @staticmethod
    async def get_message_by_id(message_id: str):
        db = MongoDB.get_db()
        messages: Collection = db["messages"]

        message = await messages.find_one({"_id": message_id})

        if message:
            message["_id"] = str(message["_id"])
        else:
            raise HTTPException(status_code=404, detail="Message not found")

        return message

    @staticmethod
    async def get_messages(conv_id: str):
        db = MongoDB.get_db()
        conversations: Collection = db["conversations"]

        conversation = conversations.find_one({"_id": conv_id})
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        db_messages: Collection = db["messages"]
        messages = db_messages.find({"conversation_id": conv_id}).to_list(length=None)

        for message in messages:
            message["_id"] = str(message["_id"])

        return messages