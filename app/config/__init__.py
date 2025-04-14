import os

from dotenv import load_dotenv

load_dotenv()
class Config:
    MONGO_URI: str = os.getenv("MONGO_URI")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY")
    SMTP_HOST: str = os.getenv("SMTP_HOST")
    SMTP_PORT: int = os.getenv("SMTP_PORT")
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD")