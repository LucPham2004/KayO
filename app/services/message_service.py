from datetime import datetime

from bson import ObjectId
from fastapi import HTTPException
from pymongo.collection import Collection

from app.config.database import MongoDB
from app.schemas.message_schema import CreateMessageSchema


class MessageService:
    @staticmethod
    def create_message(message: CreateMessageSchema):
        db = MongoDB.get_db()
        messages: Collection = db["messages"]

        message_dict = message.model_dump()
        message_dict["created_at"] = datetime.now().isoformat()

        result = messages.insert_one(message_dict)
        new_message = messages.find_one({"_id": result.inserted_id})

        if new_message:
            new_message["_id"] = str(new_message["_id"])
            new_message["conversation_id"] = str(new_message["conversation_id"])

        return new_message

    @staticmethod
    def get_message_by_id(message_id: str):
        db = MongoDB.get_db()
        messages: Collection = db["messages"]

        # Chuyển `id` sang ObjectId
        try:
            message_obj_id = ObjectId(message_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid ID format")

        message = messages.find_one({"_id": message_obj_id})

        if message:
            message["_id"] = str(message["_id"])
        else:
            raise HTTPException(status_code=404, detail="Message not found")

        return message

    @staticmethod
    def get_messages(conv_id: str):
        db = MongoDB.get_db()
        conversations: Collection = db["conversations"]

        # Chuyển `id` sang ObjectId
        try:
            conv_obj_id = ObjectId(conv_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid ID format")

        conversation = conversations.find_one({"_id": conv_obj_id})
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        db_messages: Collection = db["messages"]
        messages = db_messages.find({"conversation_id": conv_id}).sort("created_at", -1).to_list(length=None)

        for message in messages:
            message["_id"] = str(message["_id"])
            message["conversation_id"] = str(message["conversation_id"])

        return messages

    # 10 tin nhắn gần nhất trong conversation
    @staticmethod
    def get_history(conv_id: str):
        db = MongoDB.get_db()
        conversations: Collection = db["conversations"]

        # Chuyển `id` sang ObjectId
        try:
            conv_obj_id = ObjectId(conv_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid ID format")

        conversation = conversations.find_one({"_id": conv_obj_id})
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        db_messages: Collection = db["messages"]
        messages = (db_messages.find({"conversation_id": conv_id})
                    .sort("created_at", -1).limit(10).to_list(length=10))

        for message in messages:
            message["_id"] = str(message["_id"])
            message["conversation_id"] = str(message["conversation_id"])

        return messages