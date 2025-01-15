from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from uuid import UUID
from src.schema import PyObjectId, BaseModelEncoder
from typing import TypedDict
from datetime import date, datetime
class TravelCreate(BaseModel):
    destination: str = Field(min_length=2, max_length=64)
    start_date: str = Field(title="Start Date", description="Start date of the travel", format="date")
    end_date: str = Field(title="End Date", description="End date of the travel", format="date")
    total_budget: float
    activities: List[str]
    

class Place(BaseModel):
    name: str
    category: Optional[str] = None
    duration: Optional[float] = None
    visited: bool = False

class Transportation(TypedDict):
    mode: str
    cost: float
    spent_amount: float
    isCompleted: bool

class Accommodation(TypedDict):
    name: str
    cost: float
    spent_amount: float
    isCompleted: bool

class ItineraryItem(BaseModel):
    day: str
    isCompleted: bool = False
    places: List[Place] = []

class ItineraryDay(TypedDict):
    day: str
    isCompleted: bool
    places: List[Place]
    activities: List[str]
    transportation: Transportation
    accommodation: Accommodation
    mealCost: float
    budget: float
    spent_meal: float
    miscellaneous: float

class TravelResponse(BaseModelEncoder):
    id: str
    destination: str
    start_date: date
    end_date: date
    total_budget: float
    activities: List[str] = []
    itinerary: List[ItineraryItem] = []
    created_by: str
    members: List[str] = [] 
    created_at: datetime
    short_id : str
    
    class Config:
        from_attributes = True  