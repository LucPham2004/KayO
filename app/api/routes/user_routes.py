from typing import List

from fastapi import APIRouter

from app.schemas.user_schema import UserResponseSchema, UpdateUserSchema
from app.services.user_service import UserService

user_bp = APIRouter()

@user_bp.get("", response_model=UserResponseSchema)
def get_user_by_id(user_id: str):
    return UserService.get_user_by_id(user_id)

@user_bp.get("/all", response_model=List[UserResponseSchema])
def get_all():
    return UserService.get_all()

@user_bp.get("/role/user", response_model=List[UserResponseSchema])
def get_role_user():
    return UserService.get_role_user()

@user_bp.get("/role/admin", response_model=List[UserResponseSchema])
def get_admins():
    return UserService.get_admins()

@user_bp.get("/search", response_model=List[UserResponseSchema])
def search_users(keyword: str):
    return UserService.search_users_by_keyword(keyword)

@user_bp.put("/{user_id}", response_model=UserResponseSchema)
def update_user(user_id: str, update_data: UpdateUserSchema):
    return UserService.update_user(user_id, update_data.model_dump(exclude_unset=True))

@user_bp.delete("/{user_id}")
def delete_user(user_id: str):
    return UserService.delete_user(user_id)