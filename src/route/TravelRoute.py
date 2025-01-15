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
from src.model.TravelModel import Travel
from src.schema.TravelSchema import TravelResponse, TravelCreate
from datetime import datetime
from src.schema import MessageResponse
import shortuuid



router = APIRouter(prefix="/travel")


GET_ROUTE = "/"
CREATE_ROUTE = "/create"
DELETE_ROUTE = "/{short_id}"


GENRATE_ITENERARY_ROUTE = "/{short_id}/itenerary"
REVALIDATE_SHORT_ID = "/{short_id}/revalidate"
JOIN_ROUTE = "/{short_id}/join"
LEAVE_ROUTE = "/{short_id}/leave"


@router.get(GET_ROUTE, response_model=List[TravelResponse], status_code=status.HTTP_200_OK)
async def get_travels(clerk_id : str = Security(get_current_user)):
    user = User.objects(clerk_id=clerk_id).first()
    print("User: ", user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    travels = Travel.objects(Q(created_by=user.id) | Q(members__in=[user.id])).all()
    if not travels:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No travels found")
    
    travel_responses = []
    for travel in travels:
        travel_dict = travel.to_mongo().to_dict()
        travel_dict['id'] = str(travel_dict['_id'])
        travel_dict['created_by'] = str(travel_dict['created_by'])
        travel_dict['members'] = [str(member) for member in travel_dict['members']]
        travel_responses.append(TravelResponse(**travel_dict))
    return travel_responses


@router.post(CREATE_ROUTE, response_model=TravelResponse, status_code=status.HTTP_201_CREATED)
async def create_travel(travel: TravelCreate, clerk_id : str = Security(get_current_user)):
    user = User.objects(clerk_id=clerk_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    new_travel = Travel(created_by=user.id, **travel.model_dump())
    created_travel = new_travel.save()
    
    
    travel_dict = created_travel.to_mongo().to_dict()
    travel_dict['id'] = str(travel_dict['_id'])
    travel_dict['created_by'] = str(travel_dict['created_by'])
    travel_dict['members'] = [str(member) for member in travel_dict['members']]
    return TravelResponse(**travel_dict)
    
@router.post(JOIN_ROUTE, status_code=status.HTTP_200_OK, response_model=MessageResponse)
async def join_travel(short_id: str, clerk_id : str = Security(get_current_user)):
    user = User.objects(clerk_id=clerk_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    travel = Travel.objects(short_id=short_id).first()
    if not travel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Travel not found")
    
    if travel.created_by.id == user.id:
        return {"detail": "Admin already in the Group"}
    
    member_ids = [str(member.id) for member in travel.members]
    if str(user.id) in member_ids:
        return {"detail": "User Already in the Group"}
    
    travel.members.append(user.id)
    travel.save()
    
    return { "detail" : "User joined successfully" }

@router.post(LEAVE_ROUTE, status_code=status.HTTP_200_OK, response_model=MessageResponse)
async def leave_travel(short_id: str, clerk_id : str = Security(get_current_user)):
    user = User.objects(clerk_id=clerk_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    travel = Travel.objects(short_id=short_id).first()
    if not travel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Travel not found")
    
    if travel.created_by.id == user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Admin cannot leave the Group")
    
    member_ids = [str(member.id) for member in travel.members]
    if str(user.id) not in member_ids:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not in the Group")
    
    travel.members.pop(member_ids.index(str(user.id)))
    travel.save()
    
    return { "detail" : "User left successfully" }


@router.delete(DELETE_ROUTE, status_code=status.HTTP_200_OK, response_model=MessageResponse)
async def delete_travel(short_id: str, clerk_id : str = Security(get_current_user)):
    user = User.objects(clerk_id=clerk_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    travel = Travel.objects(short_id=short_id).first()
    if not travel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Travel not found")
    
    if travel.created_by.id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Member cannot delete the Group")
    
    travel.delete()
    
    return { "detail" : "Travel deleted successfully" }


@router.post(REVALIDATE_SHORT_ID, status_code=status.HTTP_200_OK, response_model=MessageResponse)
async def revalidate_short_id(short_id: str, clerk_id : str = Security(get_current_user)):
    user = User.objects(clerk_id=clerk_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    travel = Travel.objects(short_id=short_id).first()
    if not travel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Travel not found")
    
    if travel.created_by.id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Member cannot revalidate the Group")
    
    travel.short_id = shortuuid.ShortUUID().random(length=9)
    travel.save()
    
    return { "detail" : "Short Id revalidated successfully" }