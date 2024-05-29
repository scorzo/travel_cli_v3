from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List

class Accommodation(BaseModel):
    name: str = Field(description="Name of the hotel")
    address: str = Field(description="Address of the hotel")
    check_in: str = Field(description="Check-in date in ISO 8601 format")
    check_out: str = Field(description="Check-out date in ISO 8601 format")
    hotel_id: str = Field(description="Hotel ID")
    hotel_offer_id: str = Field(description="Hotel offer ID")
    price_total: str = Field(description="Total price for the stay")
    currency: str = Field(description="Currency of the price")

class Activity(BaseModel):
    activity_id: str
    name: str
    date: str
    time: str
    location: str
    purchase_url: str
    notes: str

class Transportation(BaseModel):
    type: str
    provider: str
    pickup_location: str
    dropoff_location: str
    pickup_time: str

class Destination(BaseModel):
    location: str
    latitude: float = Field(description="Latitude of the destination")
    longitude: float = Field(description="Longitude of the destination")
    arrival_date: str
    departure_date: str
    accommodation: Accommodation
    activities: List[Activity]
    transportation: List[Transportation]

class Itinerary(BaseModel):
    trip_id: str
    user_id: str
    trip_name: str
    start_date: str
    end_date: str
    destinations: List[Destination]
    notes: str
    number_of_adults: int
    number_of_children: int

