from typing import List

from fastapi import APIRouter

from app.schemas.user_schema import UserResponseSchema, UpdateUserSchema
from app.services.user_service import UserService

user_bp = APIRouter()

@user_bp.get("/{user_id}", response_model=UserResponseSchema)
def get_user_by_id(user_id: str):
    return UserService.get_user_by_id(user_id)

@user_bp.get("/all", response_model=List[UserResponseSchema])
def get_users():
    return UserService.get_users()

@user_bp.put("/{user_id}", response_model=UserResponseSchema)
def update_user(user_id: str, update_data: UpdateUserSchema):
    return UserService.update_user(user_id, update_data.model_dump(exclude_unset=True))

@user_bp.delete("/{user_id}")
def delete_user(user_id: str):
    return UserService.delete_user(user_id)