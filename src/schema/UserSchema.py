# schema/UserSchema.py
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import List, Optional
from uuid import UUID
from src.schema import PyObjectId, BaseModelEncoder

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=64)
    email: EmailStr

class UserResponse(BaseModelEncoder):
    id: PyObjectId
    name: str
    email: EmailStr
    clerk_id: str
    created_at: datetime
    groups: Optional[List[PyObjectId]] = None