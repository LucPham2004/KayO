from datetime import datetime

from fastapi import HTTPException
from pymongo.collection import Collection

from app.config.database import MongoDB
from app.schemas.conversation_schema import CreateConversationSchema


class ConversationService:
    @staticmethod
    async def create_conversation(conv: CreateConversationSchema):
        db = MongoDB.get_db()
        conversations: Collection = db["conversations"]

        conv_dict = conv.model_dump()
        conv_dict["created_at"] = datetime.now().isoformat()

        result = conversations.insert_one(conv_dict)
        new_conv = await conversations.find_one({"_id": result.inserted_id})

        if new_conv:
            new_conv["_id"] = str(new_conv["_id"])

        return new_conv

    @staticmethod
    async def get_conversations_by_user(user_id: str):
        db = MongoDB.get_db()
        users: Collection = db["users"]

        user = users.find_one({"_id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        db_conversations: Collection = db["conversations"]
        user_conversations = db_conversations.find({"user_id": user_id}).to_list(length=None)

        for conv in user_conversations:
            conv["_id"] = str(conv["_id"])

        return user_conversations

    @staticmethod
    async def get_conversations():
        db = MongoDB.get_db()
        db_conversations: Collection = db["conversations"]
        conversations = db_conversations.find().to_list(length=None)

        for conv in conversations:
            conv["_id"] = str(conv["_id"])

        return conversations