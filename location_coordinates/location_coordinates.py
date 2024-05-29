# location_module.py

from datetime import datetime
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from typing import Optional, Type
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from generic_agent import GenericAgent

class LocationQueryInput(BaseModel):
    location_description: str = Field(description="Description of the location to find coordinates for")

class LocationCoordinates(BaseModel):
    location: str = Field(description="Description of the location")
    latitude: float = Field(description="Latitude of the location")
    longitude: float = Field(description="Longitude of the location")

class LocationCoordinatesTool(BaseTool):
    name = "location_coordinates"
    description = "Useful for finding the latitude and longitude of a location based on its description"
    args_schema: Type[BaseModel] = LocationQueryInput

    def _run(
            self, location_description: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        return self.query_location_coordinates(location_description)

    async def _arun(
            self, location_description: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("location_coordinates does not support async")

    def query_location_coordinates(self, location_description: str) -> str:
        """Query the coordinates for a given location description"""

        prompt = f"Find the coordinates for {location_description} Respond with final answer using LocationCoordinates output format and only the LocationCoordinates output format."

        generic_agent = GenericAgent(model_name="gpt-4o", pydantic_model=LocationCoordinates, tools=[])

        result = generic_agent.generate_response(prompt)

        return result

# Example usage
if __name__ == "__main__":
    location_description = "Paris, France"
    location_tool = LocationCoordinatesTool()
    coordinates = location_tool._run(location_description)
    print(coordinates)
