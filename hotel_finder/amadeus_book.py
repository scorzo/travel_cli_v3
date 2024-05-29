from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from typing import Optional, Type, List, Dict, Any
import os
import requests

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

class HotelBookingParams(BaseModel):
    offer_id: str = Field(description="Offer ID for hotel booking")
    guests: List[Dict[str, Any]] = Field(description="Guest information for booking")
    payment: Dict[str, Any] = Field(description="Payment information for booking")

class AmadeusHotelBookingTool(BaseTool):
    name = "amadeus_hotel_booking"
    description = "Useful for booking hotels using the Amadeus API"
    args_schema: Type[BaseModel] = HotelBookingParams

    def _run(
            self, offer_id: str, guests: List[Dict[str, Any]], payment: Dict[str, Any], run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> Dict[str, Any]:
        """Use the tool."""
        return self.book_hotel(offer_id, guests, payment)

    async def _arun(
            self, offer_id: str, guests: List[Dict[str, Any]], payment: Dict[str, Any], run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> Dict[str, Any]:
        """Use the tool asynchronously."""
        raise NotImplementedError("amadeus_hotel_booking does not support async")

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

    def book_hotel(self, offer_id: str, guests: List[Dict[str, Any]], payment: Dict[str, Any]) -> Dict[str, Any]:
        """Book a hotel offer"""
        api_key = os.environ.get('AMADEUS_API_KEY')
        api_secret = os.environ.get('AMADEUS_API_SECRET')
        base_url = "https://test.api.amadeus.com/v1/booking/hotel-bookings"  # Use "https://api.amadeus.com" for production

        if not api_key or not api_secret:
            return "Amadeus API key and secret must be set in environment variables."

        access_token = self.get_access_token(api_key, api_secret)
        if not access_token:
            return "Failed to retrieve access token."

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "offerId": offer_id,
            "guests": guests,
            "payments": [payment]
        }
        response = requests.post(base_url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Failed to book hotel: {response.status_code}"

# Example usage
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    booking_tool = AmadeusHotelBookingTool()

    booking_params = HotelBookingParams(
        offer_id="OFFER_ID",  # Example offer ID
        guests=[{
            "name": {"firstName": "John", "lastName": "Doe"},
            "contact": {"phone": "+1234567890", "email": "john.doe@example.com"}
        }],
        payment={
            "method": "creditCard",
            "card": {
                "vendorCode": "VI",
                "cardNumber": "4111111111111111",
                "expiryDate": "2023-12"
            }
        }
    )

    confirmation = booking_tool._run(
        offer_id=booking_params.offer_id,
        guests=booking_params.guests,
        payment=booking_params.payment
    )
    print("Booking Confirmation:", confirmation)
