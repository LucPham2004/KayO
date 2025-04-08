from datetime import datetime, timedelta

from fastapi import HTTPException
from app.config.database import MongoDB
from pymongo.collection import Collection

from app.schemas.auth_schema import (
    LoginSchema, 
    RegisterSchema, 
    ForgotPasswordSchema,
    VerifyOTPSchema,
    ResetPasswordSchema
)
from app.utils.auth_utils import (
    verify_password, 
    create_access_token, 
    hash_password, 
    generate_otp, 
    send_otp_email
)


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

    @staticmethod
    def forgot_password(request: ForgotPasswordSchema):
        db = MongoDB.get_db()
        users: Collection = db["users"]
        otps: Collection = db["otps"]

        if "expires_at_1" not in otps.index_information():
            otps.create_index("expires_at", expireAfterSeconds=180)  # 180 seconds = 3 minutes

        
        user = users.find_one({"email": request.email})
        if not user:
            raise HTTPException(status_code=404, detail="Email not found")

        otp = generate_otp()
        expires_at = datetime.now() + timedelta(minutes=3)

        otp_data = {
            "email": request.email,
            "otp": otp,
            "expires_at": expires_at,
            "created_at": datetime.now()
        }
        otps.insert_one(otp_data)

        if not send_otp_email(request.email, otp):
            raise HTTPException(status_code=500, detail="Gửi OTP thất bại")

        return {
            "message": "OTP gửi thành công"
        }

    @staticmethod
    def verify_otp(request: VerifyOTPSchema):
        db = MongoDB.get_db()
        otps: Collection = db["otps"]

        otp_record = otps.find_one(
            {
                "email": request.email,
                "otp": request.otp,
                "expires_at": {"$gt": datetime.now()}
            },
            sort=[("created_at", -1)]
        )

        if not otp_record:
            return {
                "message": "Mã OTP không hợp lệ hoặc đã hết hạn",
                "is_valid": False
            }

        return {
            "message": "Mã OTP hợp lệ",
            "is_valid": True
        }

    @staticmethod
    def reset_password(request: ResetPasswordSchema):
        db = MongoDB.get_db()
        users: Collection = db["users"]
        otps: Collection = db["otps"]

        otp_record = otps.find_one(
            {
                "email": request.email,
                "otp": request.otp,
                "expires_at": {"$gt": datetime.now()}
            },
            sort=[("created_at", -1)]
        )

        if not otp_record:
            raise HTTPException(status_code=400, detail="Mã OTP không hợp lệ hoặc đã hết hạn")
    
        hashedPassword = hash_password(request.newPassword)

        users.update_one(
            {"email": request.email},
            {"$set": {"password": hashedPassword}}
        )

        otps.delete_one({"_id": otp_record["_id"]})

        return {
            "message": "Đặt lại mật khẩu thành công"
        }