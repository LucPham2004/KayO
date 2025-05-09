from datetime import datetime

from bson import ObjectId
from fastapi import HTTPException
from pymongo.collection import Collection

from app.config.database import MongoDB
from app.schemas.conversation_schema import CreateConversationSchema


class ConversationService:
    @staticmethod
    def create_conversation(conv: CreateConversationSchema):
        db = MongoDB.get_db()
        conversations: Collection = db["conversations"]

        conv_dict = conv.model_dump()
        conv_dict["created_at"] = datetime.now().isoformat()
        conv_dict["update_at"] = datetime.now().isoformat()

        result = conversations.insert_one(conv_dict)
        new_conv = conversations.find_one({"_id": result.inserted_id})

        if new_conv:
            new_conv["_id"] = str(new_conv["_id"])

        return new_conv

    @staticmethod
    def get_conversation_by_id(id: str):
        db = MongoDB.get_db()
        conversations: Collection = db["conversations"]

        # Chuyển `id` sang ObjectId
        try:
            obj_id = ObjectId(id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid conversation ID format")

        conversation = conversations.find_one({"_id": obj_id})
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation with id: " + id + " not found")

        conversation["_id"] = str(conversation["_id"])

        return conversation

    @staticmethod
    def get_conversations_by_user(user_id: str):
        db = MongoDB.get_db()
        users: Collection = db["users"]

        # Chuyển `id` sang ObjectId
        try:
            user_obj_id = ObjectId(user_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid ID format")

        user = users.find_one({"_id": user_obj_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        db_conversations: Collection = db["conversations"]
        user_conversations = db_conversations.find({"user_id": user_id}).to_list(length=None)

        for conv in user_conversations:
            conv["_id"] = str(conv["_id"])

        return user_conversations

    @staticmethod
    def search_conversations_by_keyword(user_id: str, keyword: str):
        db = MongoDB.get_db()
        users: Collection = db["users"]

        try:
            user_obj_id = ObjectId(user_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid ID format")

        user = users.find_one({"_id": user_obj_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        db_conversations: Collection = db["conversations"]

        query = {
            "user_id": user_id,
            "name": {"$regex": keyword, "$options": "i"}
        }

        matched_conversations = db_conversations.find(query).to_list(length=None)

        for conv in matched_conversations:
            conv["_id"] = str(conv["_id"])

        return matched_conversations

    @staticmethod
    def get_conversations():
        db = MongoDB.get_db()
        db_conversations: Collection = db["conversations"]
        conversations = db_conversations.find().to_list(length=None)

        for conv in conversations:
            conv["_id"] = str(conv["_id"])

        return conversations

    @staticmethod
    def update_conversation(id: str, update_data: dict):
        db = MongoDB.get_db()
        conversations: Collection = db["conversations"]

        try:
            obj_id = ObjectId(id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid conversation ID format")

        conversation = conversations.find_one({"_id": obj_id})
        conversation["name"] = update_data["name"]
        conversation["update_at"] = datetime.now().isoformat()

        result = conversations.update_one({"_id": obj_id}, {"$set": conversation})

        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail=f"Conversation with id: {id} not found")

        return ConversationService.get_conversation_by_id(id)

    @staticmethod
    def delete_conversation(id: str):
        db = MongoDB.get_db()
        conversations: Collection = db["conversations"]

        try:
            obj_id = ObjectId(id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid conversation ID format")

        result = conversations.delete_one({"_id": obj_id})

        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail=f"Conversation with id: {id} not found")

        return {"message": "Conversation deleted successfully"}