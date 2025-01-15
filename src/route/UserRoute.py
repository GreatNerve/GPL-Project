# route/UserRoute.py
from fastapi import APIRouter, HTTPException, status, Depends, Security
from typing import Annotated
from src.model.UserModel import User
from src.schema.UserSchema import UserCreate, UserResponse
from mongoengine.queryset.visitor import Q
from bson import ObjectId
from mongoengine.connection import get_connection, get_db
from src.dependencies.getCurrentUser import get_current_user
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List
from src.model.UserModel import User


router = APIRouter(prefix="/user")
GET_ROUTE = "/"
CREATE_ROUTE = "/create"

@router.get(GET_ROUTE, response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_users(clerk_id : str = Security(get_current_user)):
    users = User.objects(clerk_id=clerk_id).first()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
    return users
    

@router.post(CREATE_ROUTE, response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, clerk_id : str = Security(get_current_user)):
    user_email = user.email
    existing_user = User.objects(Q(email=user_email) | Q(clerk_id=clerk_id)).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    new_user = User(clerk_id=clerk_id, **user.model_dump())
    created_user = new_user.save()
    return created_user



    clerk_id = get_current_user(credentials)
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
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Duplicate key error")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")