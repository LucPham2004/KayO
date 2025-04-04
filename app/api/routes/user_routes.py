from typing import List

from fastapi import APIRouter

from app.schemas.user_schema import UserResponseSchema
from app.services.user_service import UserService

user_bp = APIRouter()

@user_bp.get("/{user_id}", response_model=UserResponseSchema)
def get_user_by_id(user_id: str):
    return UserService.get_user_by_id(user_id)

@user_bp.get("/all", response_model=List[UserResponseSchema])
def get_users():
    return UserService.get_users()