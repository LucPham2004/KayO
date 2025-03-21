from fastapi import HTTPException
from app.config.database import MongoDB
from pymongo.collection import Collection


class UserService:
    @staticmethod
    def login(username, password):
        db = MongoDB.get_db()
        users: Collection = db["users"]

        user = users.find_one({"username": username, "password": password})
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        user["_id"] = str(user["_id"])  # Chuyển ObjectId thành string
        user.pop("password", None)  # Loại bỏ trường password

        return {
            "message": "Login successful",
            "user" : user
        }

    @staticmethod
    def register(username, password):
        db = MongoDB.get_db()
        users: Collection = db["users"]

        if users.find_one({"username": username}):
            raise HTTPException(status_code=400, detail="User already exists")

        user_data = {"username": username, "password": password}  # TODO: Hash password sau này
        result = users.insert_one(user_data)

        return {
            "message": "register success",
            "_id": str(result.inserted_id)
        }