# route/UserRoute.py
from fastapi import APIRouter, HTTPException, status, Depends
from model.UserModel import User
from schema.UserSchema import UserCreate, UserResponse
from mongoengine.queryset.visitor import Q
from bson import ObjectId
from mongoengine.connection import get_connection, get_db
from middleware.AuthMiddleware import AuthMiddleware
from typing import List

auth_middleware = AuthMiddleware()

router = APIRouter()
GET_ROUTE = "/"
CREATE_ROUTE = "/create"
UPDATE_ROUTE = "/{user_id}"


@router.get(GET_ROUTE, response_model=List[UserResponse], status_code=status.HTTP_200_OK)
async def get_users():
    users = User.objects().all()
    return users

@router.post(CREATE_ROUTE, response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    user_email = user.email
    user_app_write_id = user.user_app_write_id
    existing_user = User.objects(Q(email=user_email) | Q(user_app_write_id=user_app_write_id)).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    new_user = User(**user.model_dump())
    created_user = new_user.save()
    return created_user


@router.put(UPDATE_ROUTE, response_model=UserResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(auth_middleware)])
async def update_user(user_id: str, user: UserCreate):
    if not ObjectId.is_valid(user_id):
        raise ValueError("Invalid ObjectId format")
    object_id = ObjectId(user_id)
    existing_user = User.objects(id=object_id).first()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    try:
        existing_user.update(**user.model_dump())
        updated_user = User.objects(id=object_id).first()
        return updated_user
    except Exception as e:
        if "duplicate key error" in str(e):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email or App Write ID already linked to another user")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))