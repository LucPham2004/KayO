from datetime import datetime

from bson import ObjectId
from fastapi import HTTPException
from pymongo.collection import Collection

from app.config.database import MongoDB


class UserService:
    @staticmethod
    def get_user_by_id(id: str):
        db = MongoDB.get_db()
        users: Collection = db["users"]

        # Chuyển `id` sang ObjectId
        try:
            obj_id = ObjectId(id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid user ID format")

        user = users.find_one({"_id": obj_id})
        if not user:
            raise HTTPException(status_code=404, detail="User with id: " + id + " not found")

        user["_id"] = str(user["_id"])

        return user

    @staticmethod
    def get_users():
        db = MongoDB.get_db()
        db_users: Collection = db["users"]

        users = db_users.find().to_list(length=None)

        for user in users:
            user["_id"] = str(user["_id"])

        return users

    @staticmethod
    def update_user(id: str, update_data: dict):
        db = MongoDB.get_db()
        users: Collection = db["users"]

        try:
            obj_id = ObjectId(id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid user ID format")

        update_data["updated_at"] = datetime.now().isoformat()

        result = users.update_one({"_id": obj_id}, {"$set": update_data})

        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail=f"User with id: {id} not found")

        return UserService.get_user_by_id(id)

    @staticmethod
    def delete_user(id: str):
        db = MongoDB.get_db()
        users: Collection = db["users"]

        try:
            obj_id = ObjectId(id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid user ID format")

        result = users.delete_one({"_id": obj_id})

        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail=f"User with id: {id} not found")

        return {"message": "User deleted successfully"}