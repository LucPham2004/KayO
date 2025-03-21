from fastapi import FastAPI
from app.api.routes import register_routes
from app.config.database import MongoDB

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello, kayO!"}

# Kết nối mongodb
MongoDB.connect()

# Đăng ký các route
register_routes(app)

