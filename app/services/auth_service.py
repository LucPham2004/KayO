from datetime import datetime, timedelta

from bson.objectid import ObjectId
from pymongo.collection import Collection

from app.config.database import MongoDB
from app.schemas.auth_schema import (
    LoginSchema,
    RegisterSchema,
    ForgotPasswordSchema,
    VerifyOTPSchema,
    ResetPasswordSchema,
    ChangePasswordSchema
)
from app.utils.auth_utils import (
    verify_password,
    create_access_token,
    hash_password,
    generate_otp,
    send_otp_email,
    decode_token
)


class UserService:
    @staticmethod
    def login(login: LoginSchema):
        db = MongoDB.get_db()
        users: Collection = db["users"]

        user = users.find_one({"email": login.email})
        if not user or not verify_password(login.password, user['password']):
            return {
                "message": "Email hoặc mật khẩu không chính xác!",
                "user": None,
                "access_token": None,
                "is_valid": False
            }

        # Tạo dữ liệu user để trả về
        user_data = {
            "id": str(user["_id"]),  # Chuyển ObjectId sang string
            "email": user["email"],
            "username": user["username"]
        }

        # Tạo JWT token
        token_data = {
            "sub": user_data["id"],
            "email": user_data["email"],
            "username": user_data["username"]
        }

        # Tạo token không có thời hạn
        access_token = create_access_token(token_data)

        return {
            "message": "Đăng nhập thành công",
            "user": user_data,
            "access_token": access_token,
            "is_valid": True
        }

    @staticmethod
    def register(register: RegisterSchema):
        db = MongoDB.get_db()
        users: Collection = db["users"]

        # Kiểm tra xem email đã tồn tại chưa
        if users.find_one({"email": register.email}):
            return {
                "message": "Email đã tồn tại",
                "_id": None,
                "is_valid": False
            }

        # hash password
        hashed_password = hash_password(register.password)

        user_data = {
            "email": register.email,
            "username": register.username,
            "password": hashed_password,
            "role": "USER",
            "created_at": datetime.now().isoformat(),
            "update_at": datetime.now().isoformat()
        }

        result = users.insert_one(user_data)

        return {
            "message": "Đăng ký thành công",
            "_id": str(result.inserted_id),
            "is_valid": True
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
            return {
                "message": "Email không tồn tại",
                "is_valid": False
            }

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
            return {
                "message": "Gửi OTP thất bại",
                "is_valid": False
            }

        return {
            "message": "Gửi OTP thành công",
            "is_valid": True
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
            return {
                "message": "Mã OTP không hợp lệ hoặc đã hết hạn",
                "is_valid": False
            }
        
        if(request.newPassword != request.confirmPassword):
            return {
                "message": "Mật khẩu không khớp",
                "is_valid": False
            }   
    
        hashedPassword = hash_password(request.newPassword)

        users.update_one(
            {"email": request.email},
            {"$set": {"password": hashedPassword}}
        )

        otps.delete_one({"_id": otp_record["_id"]})

        return {
            "message": "Đặt lại mật khẩu thành công",
            "is_valid": True
        }

    @staticmethod
    def get_account(authorization: str):
        # Kiểm tra và lấy token từ header
        if not authorization or not authorization.startswith("Bearer "):
            return {
                "message": "Token không hợp lệ",
                "user": None,
                "is_valid": False
            }
        
        try:
            token = authorization.split(" ")[1]
            
            # Decode token
            payload = decode_token(token)
            if not payload:
                return {
                    "message": "Token không hợp lệ hoặc đã hết hạn",
                    "user": None,
                    "is_valid": False
                }
            
            # Lấy thông tin user từ database
            db = MongoDB.get_db()
            users: Collection = db["users"]
            
            user = users.find_one({"_id": ObjectId(payload["sub"])})
            if not user:
                return {
                    "message": "Người dùng không tồn tại",
                    "user": None,
                    "is_valid": False
                }
            
            # Tạo dữ liệu user để trả về
            user_data = {
                "id": str(user["_id"]),
                "email": user["email"],
                "username": user["username"]
            }
            
            return {
                "message": "Lấy thông tin tài khoản thành công",
                "user": user_data,
                "is_valid": True
            }
        except Exception as e:
            print(f"Error in get_account: {str(e)}")
            return {
                "message": "Có lỗi xảy ra khi lấy thông tin tài khoản",
                "user": None,
                "is_valid": False
            }

    @staticmethod
    def change_password(request: ChangePasswordSchema, authorization: str):
        # Kiểm tra và lấy token từ header
        if not authorization or not authorization.startswith("Bearer "):
            return {
                "message": "Token không hợp lệ",
                "is_valid": False
            }
        
        try:
            token = authorization.split(" ")[1]
            
            # Decode token
            payload = decode_token(token)
            if not payload:
                return {
                    "message": "Token không hợp lệ hoặc đã hết hạn",
                    "is_valid": False
                }
            
            # Lấy thông tin user từ database
            db = MongoDB.get_db()
            users: Collection = db["users"]
            
            user = users.find_one({"_id": ObjectId(payload["sub"])})
            if not user:
                return {
                    "message": "Người dùng không tồn tại",
                    "is_valid": False
                }
            
            # Kiểm tra mật khẩu hiện tại
            if not verify_password(request.current_password, user["password"]):
                return {
                    "message": "Mật khẩu hiện tại không chính xác",
                    "is_valid": False
                }
            
            # Hash mật khẩu mới
            hashed_password = hash_password(request.new_password)
            
            # Cập nhật mật khẩu mới
            users.update_one(
                {"_id": ObjectId(payload["sub"])},
                {"$set": {"password": hashed_password}}
            )
            
            return {
                "message": "Đổi mật khẩu thành công",
                "is_valid": True
            }
            
        except Exception as e:
            print(f"Error in change_password: {str(e)}")
            return {
                "message": "Có lỗi xảy ra khi đổi mật khẩu",
                "is_valid": False
            }