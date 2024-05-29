from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from typing import Optional, Type, List, Dict, Any
import os
import requests

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

class HotelOffersParams(BaseModel):
    hotel_ids: List[str] = Field(description="List of hotel IDs for offer search")
    start_date: str = Field(description="Start date for hotel search in ISO 8601 format")
    end_date: str = Field(description="End date for hotel search in ISO 8601 format")
    number_of_adults: int
    number_of_children: int

class AmadeusHotelOffersTool(BaseTool):
    name = "amadeus_hotel_offers"
    description = "Useful for searching hotel offers using the Amadeus API"
    args_schema: Type[BaseModel] = HotelOffersParams

    def _run(
            self, hotel_ids: List[str], start_date: str, end_date: str, number_of_adults: int, number_of_children: int, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> List[Dict[str, Any]]:
        """Use the tool."""
        return self.hotel_offers(hotel_ids, start_date, end_date, number_of_adults, number_of_children)

    async def _arun(
            self, hotel_ids: List[str], start_date: str, end_date: str, number_of_adults: int, number_of_children: int, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> List[Dict[str, Any]]:
        """Use the tool asynchronously."""
        raise NotImplementedError("amadeus_hotel_offers does not support async")

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

    def hotel_offers(self, hotel_ids: List[str], start_date: str, end_date: str, number_of_adults: int, number_of_children: int) -> List[Dict[str, Any]]:
        """Get hotel offers based on hotel IDs and booking parameters"""
        api_key = os.environ.get('AMADEUS_API_KEY')
        api_secret = os.environ.get('AMADEUS_API_SECRET')
        base_url = "https://test.api.amadeus.com/v3/shopping/hotel-offers"  # Use "https://api.amadeus.com" for production

        if not api_key or not api_secret:
            return "Amadeus API key and secret must be set in environment variables."

        access_token = self.get_access_token(api_key, api_secret)
        if not access_token:
            return "Failed to retrieve access token."

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        hotel_ids = hotel_ids[:10]  # Truncate the list to the first 10 hotel IDs
        query_params = {
            "hotelIds": ','.join(hotel_ids),
            "checkInDate": start_date,
            "checkOutDate": end_date,
            "adults": number_of_adults
            #"childAges": ','.join(['10'] * number_of_children)  # Assuming average child age of 10
        }

        # Print the request details for verbosity
        print("Request URL:", base_url)
        print("Request Headers:", headers)
        print("Request Parameters:", query_params)

        response = requests.get(base_url, headers=headers, params=query_params)

        # Print the response status and content for verbosity
        print("Response Status Code:", response.status_code)
        print("Response Content:", response.content)

        if response.status_code == 200:
            data = response.json()
            return data['data']
        else:
            return f"Failed to retrieve data: {response.status_code}"


# Example usage
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    hotel_offers_tool = AmadeusHotelOffersTool()

    offers_params = HotelOffersParams(
        hotel_ids=["HOTEL_ID_1", "HOTEL_ID_2"],  # Example hotel IDs
        start_date="2024-06-01",
        end_date="2024-06-10",
        number_of_adults=2,
        number_of_children=1
    )

    offers = hotel_offers_tool._run(
        hotel_ids=offers_params.hotel_ids,
        start_date=offers_params.start_date,
        end_date=offers_params.end_date,
        number_of_adults=offers_params.number_of_adults,
        number_of_children=offers_params.number_of_children
    )
    print("Hotel Offers:", offers)
