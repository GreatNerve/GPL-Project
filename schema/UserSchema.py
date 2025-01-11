# schema/UserSchema.py
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import List, Optional
from uuid import UUID
from schema import PyObjectId, BaseModelEncoder

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=64)
    email: EmailStr
    user_app_write_id: UUID

class UserResponse(BaseModelEncoder):
    id: PyObjectId
    name: str
    email: EmailStr
    user_app_write_id: UUID
    created_at: datetime
    groups: Optional[List[PyObjectId]] = None