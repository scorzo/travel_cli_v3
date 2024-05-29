from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List

class ActivityRequest(BaseModel):
    name: str

class DestinationRequest(BaseModel):
    location: str
    latitude: float = Field(description="Latitude of the destination")
    longitude: float = Field(description="Longitude of the destination")
    activities: List[ActivityRequest]

class ItineraryRequest(BaseModel):
    start_date: str
    end_date: str
    destinations: List[DestinationRequest]
    number_of_adults: int
    number_of_children: int


