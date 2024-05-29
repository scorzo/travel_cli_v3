from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from typing import Optional, Type, List
import os
import requests

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

class HotelListParams(BaseModel):
    latitude: float = Field(description="Latitude for hotel search")
    longitude: float = Field(description="Longitude for hotel search")
    radius: int = Field(description="Radius in kilometers for hotel search")

class AmadeusHotelListTool(BaseTool):
    name = "amadeus_hotel_list"
    description = "Useful for listing hotels using the Amadeus API"
    args_schema: Type[BaseModel] = HotelListParams

    def _run(
            self, latitude: float, longitude: float, radius: int, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> List[str]:
        """Use the tool."""
        return self.hotels_list(latitude, longitude, radius)

    async def _arun(
            self, latitude: float, longitude: float, radius: int, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> List[str]:
        """Use the tool asynchronously."""
        raise NotImplementedError("amadeus_hotel_list does not support async")

    def get_access_token(self, api_key: str, api_secret: str) -> Optional[str]:
        url = "https://test.api.amadeus.com/v1/security/oauth2/token"  # Use "https://api.amadeus.com" for production
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "client_credentials",
            "client_id": api_key,
            "client_secret": api_secret
        }
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json().get("access_token")
        return None

    def hotels_list(self, latitude: float, longitude: float, radius: int) -> List[str]:
        """Get list of hotel IDs based on location and radius"""
        api_key = os.environ.get('AMADEUS_API_KEY')
        api_secret = os.environ.get('AMADEUS_API_SECRET')
        base_url = "https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-geocode"  # Use "https://api.amadeus.com" for production

        if not api_key or not api_secret:
            return "Amadeus API key and secret must be set in environment variables."

        access_token = self.get_access_token(api_key, api_secret)
        if not access_token:
            return "Failed to retrieve access token."

        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        query_params = {
            "latitude": latitude,
            "longitude": longitude,
            "radius": radius
        }
        response = requests.get(base_url, headers=headers, params=query_params)
        if response.status_code == 200:
            data = response.json()
            hotel_ids = [hotel['hotelId'] for hotel in data['data']]
            hotel_ids = hotel_ids[:10]  # Truncate the list to the first 10 hotel IDs
            return hotel_ids
        else:
            return f"Failed to retrieve data: {response.status_code}"

# Example usage
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    hotel_list_tool = AmadeusHotelListTool()

    list_params = HotelListParams(
        latitude=48.8566,
        longitude=2.3522,
        radius=10,
    )

    hotel_ids = hotel_list_tool._run(
        latitude=list_params.latitude,
        longitude=list_params.longitude,
        radius=list_params.radius,
    )
    print("Hotel IDs:", hotel_ids)
