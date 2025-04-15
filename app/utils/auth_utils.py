from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.config import Config

# Cấu hình passlib để sử dụng bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    SECRET_KEY = Config.SECRET_KEY
    ALGORITHM = "HS256"

    """Tạo JWT token với dữ liệu."""
    to_encode = data.copy()
    # Bỏ phần thêm thời gian hết hạn
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))

def send_otp_email(email: str, otp: str):
    msg = MIMEMultipart()
    msg['From'] = Config.SMTP_USERNAME
    msg['To'] = email
    msg['Subject'] = "Yêu cầu đặt lại mật khẩu"

    body = f"""
    <html>
        <body>
            <h2>Yêu cầu đặt lại mật khẩu</h2>
            <p>Mã OTP của bạn là: <strong>{otp}</strong></p>
            <p>Mã OTP sẽ hết hạn trong 3 phút.</p>
            <p>Nếu bạn không yêu cầu đặt lại mật khẩu, vui lòng bỏ qua email này.</p>
        </body>
    </html>
    """
    
    msg.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP(Config.SMTP_HOST, Config.SMTP_PORT)
        server.starttls()
        server.login(Config.SMTP_USERNAME, Config.SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Gửi OTP thất bại: {str(e)}")
        return False

def decode_token(token: str):
    SECRET_KEY = Config.SECRET_KEY
    ALGORITHM = "HS256"
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        return None