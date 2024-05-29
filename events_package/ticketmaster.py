from datetime import datetime
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from typing import Optional, Type
import os
import requests

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

class TicketmasterQueryInput(BaseModel):
    keyword: str = Field(description="Keyword for event search")
    location: str = Field(description="Location for event search")
    start_date: str = Field(description="Start date for event search in ISO 8601 format")
    end_date: str = Field(description="End date for event search in ISO 8601 format")

class TicketmasterEventsTool(BaseTool):
    name = "ticketmaster_events"
    description = "Useful for querying Ticketmaster for scheduled event listings and dates"
    args_schema: Type[BaseModel] = TicketmasterQueryInput

    def _run(
            self, keyword: str, location: str, start_date: str, end_date: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        return self.query_ticketmaster_events(keyword, location, start_date, end_date)

    async def _arun(
            self, keyword: str, location: str, start_date: str, end_date: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("ticketmaster_events does not support async")

    def query_ticketmaster_events(self, keyword: str, location: str, start_date: str, end_date: str) -> str:
        """Query Ticketmaster events API for scheduled event listings and dates"""

        print(f"Received arguments - Keyword: {keyword}, Location: {location}, Start Date: {start_date}, End Date: {end_date}")

        # Convert start_date and end_date from ISO 8601 string to datetime objects if they are not already
        if isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        if isinstance(end_date, str):
            end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))

        base_url = "https://app.ticketmaster.com/discovery/v2/events.json"
        params = {
            'apikey': os.environ['TICKETMASTER_API_KEY'],
            'keyword': keyword,
            'locale': '*',
            'city': location,
            'startDateTime': datetime.strftime(start_date, "%Y-%m-%dT%H:%M:%SZ"),
            'endDateTime': datetime.strftime(end_date, "%Y-%m-%dT%H:%M:%SZ")
        }

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data['page']['totalElements'] == 0:
                return "No events found for the specified query."
            return data
        else:
            return f"Failed to retrieve data: {response.status_code}"


