from datetime import datetime, timedelta

from fastapi import HTTPException
from app.config.database import MongoDB
from pymongo.collection import Collection

from app.schemas.auth_schema import LoginSchema, RegisterSchema
from app.utils.auth_utils import verify_password, create_access_token, hash_password


class UserService:
    @staticmethod
    def login(login: LoginSchema):
        db = MongoDB.get_db()
        users: Collection = db["users"]

        user = users.find_one({"email": login.email})
        if not user or not verify_password(login.password, user['password']):
            raise HTTPException(status_code=401, detail="Email or password incorrect!")

        # Chuyển _id thành string và loại bỏ password khỏi phản hồi
        user["_id"] = str(user["_id"])
        user.pop("password", None)

        # Tạo JWT token
        token_data = {
            "sub": user["_id"],  # Subject là user_id
            "email": user["email"],
            "username": user["username"]
        }

        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token( token_data, access_token_expires)

        return {
            "message": "Login successfully",
            "access_token": access_token,
            "user": user
        }

    @staticmethod
    def register(register: RegisterSchema):
        db = MongoDB.get_db()
        users: Collection = db["users"]

        # Kiểm tra xem email đã tồn tại chưa
        if users.find_one({"email": register.email}):
            raise HTTPException(status_code=400, detail="Email already exists")

        # hash password
        hashed_password = hash_password(register.password)

        user_data = {
            "email": register.email,
            "username": register.username,
            "password": hashed_password,
            "created_at": datetime.now().isoformat()
        }

        result = users.insert_one(user_data)

        return {
            "message": "register success",
            "_id": str(result.inserted_id)
        }