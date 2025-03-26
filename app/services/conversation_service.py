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

        conv = conv.model_dump()
        conv["created_at"] = datetime.now().isoformat()

        result = conversations.insert_one(conv)
        new_conv = await conversations.find_one({"_id": result.inserted_id})

        if new_conv:
            new_conv["_id"] = str(new_conv["_id"])

        return new_conv

    @staticmethod
    async def get_conversations(user_id: str):
        db = MongoDB.get_db()
        users: Collection = db["users"]

        user = users.find_one({"_id": user_id})
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        db_conversations: Collection = db["conversations"]
        user_conversations = db_conversations.find({"user_id": user_id}).to_list(length=None)

        for convo in user_conversations:
            convo["_id"] = str(convo["_id"])

        return user_conversations