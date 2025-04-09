from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import register_routes
from app.config.database import MongoDB

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Cho phép các domain này
    allow_credentials=True,
    allow_methods=["*"],              # Cho phép tất cả phương thức (GET, POST, ...)
    allow_headers=["*"],              # Cho phép tất cả header
)

@app.get("/")
def home():
    return {"message": "Hello, kayO!"}

# Kết nối mongodb
MongoDB.connect()

# Đăng ký các route
register_routes(app)

