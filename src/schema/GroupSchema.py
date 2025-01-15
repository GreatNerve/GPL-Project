# from typing import List, Optional
# from pydantic import BaseModel
# from datetime import datetime
# from bson import ObjectId
# import uuid
#
# class GroupCreateSchema(BaseModel):
#     name: str
#     description: Optional[str] = None
#     members: ObjectId
#     created_by: ObjectId
#
# class GroupResponseSchema(BaseModel):
#     id: uuid.UUID
#     name: str
#     description: Optional[str] = None
#     members: ObjectId
#     created_by: ObjectId
#     created_at: datetime
#
#     class Config:
#         arbitrary_types_allowed = True