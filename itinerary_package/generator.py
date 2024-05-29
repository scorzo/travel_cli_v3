from .models import Itinerary, Destination, Accommodation, Activity, Transportation
from .models_request import ItineraryRequest
from events_package.ticketmaster import TicketmasterEventsTool
from hotel_finder.amadeus_list import AmadeusHotelListTool
from hotel_finder.amadeus_offers import AmadeusHotelOffersTool
from location_coordinates.location_coordinates import LocationCoordinatesTool

from generic_agent import GenericAgent

def generate_sample_itinerary():
    """
    Generates a sample itinerary with hardcoded data.

    Returns:
        str: A JSON string representing the itinerary.

    Example:
        >>> from itinerary_package import generate_sample_itinerary
        >>> print(generate_sample_itinerary())
    """

    # This function returns a sample itinerary as a JSON string
    itinerary = Itinerary(
        trip_id="123456",
        user_id="user_7890",
        trip_name="Summer Vacation",
        start_date="2024-07-01",
        end_date="2024-07-14",
        destinations=[Destination(
            location="Paris, France",
            arrival_date="2024-07-01",
            departure_date="2024-07-05",
            accommodation=Accommodation(
                name="Hotel Paris",
                address="123 Paris St, Paris, France",
                check_in="2024-07-01T15:00",
                check_out="2024-07-05T11:00"
            ),
            activities=[Activity(
                activity_id="1",
                name="Eiffel Tower Visit",
                date="2024-07-02",
                time="10:00",
                location="Champ de Mars, 5 Avenue Anatole France, 75007 Paris, France",
                notes="Pre-book tickets online."
            )],
            transportation=[Transportation(
                type="Taxi",
                provider="Paris Taxi",
                pickup_location="Hotel Paris",
                dropoff_location="Eiffel Tower",
                pickup_time="2024-07-02T09:30"
            )]
        )],
        notes="Remember to check the weather and pack accordingly."
    )
    return itinerary.json()

def generate_itinerary_from_model_with_tools(prompt, model_name="gpt-4o", pydantic_model=Itinerary, tools=[TicketmasterEventsTool(), AmadeusHotelListTool(), AmadeusHotelOffersTool(), LocationCoordinatesTool()]):
    """
    Generates an itinerary based on a user-provided prompt using a specified language model.

    Args:
        prompt (str): The prompt to send to the language model.
        model_name (str): The name of the model to use, defaults to 'gpt-4o'.
        pydantic_model (Pydantic Model): The Pydantic model to use for structured output.
        tools (list): A list of functions to use for post-processing.

    Returns:
        dict: A dictionary representation of the generated itinerary.

    Example:
        >>> details = generate_itinerary_from_model_with_tools("Create an itinerary for a summer vacation in Hawaii")
        >>> print(details)
    """

    # Create an instance of GenericAgent
    generic_agent = GenericAgent(model_name=model_name, pydantic_model=pydantic_model, tools=tools)

    append_this = "  Respond with final answer using Itinerary output format and only the Itinerary output format."

    # Append the string
    prompt += append_this

    # Generate the response using the agent
    result = generic_agent.generate_response(prompt)

    return result


def generate_itinerary_request_from_model_with_tools(prompt, model_name="gpt-4o", pydantic_model=ItineraryRequest, tools=[LocationCoordinatesTool()]):
    """
    Generates an itinerary based on a user-provided prompt using a specified language model.

    Args:
        prompt (str): The prompt to send to the language model.
        model_name (str): The name of the model to use, defaults to 'gpt-4o'.
        pydantic_model (Pydantic Model): The Pydantic model to use for structured output.
        tools (list): A list of functions to use for post-processing.

    Returns:
        dict: A dictionary representation of the generated itinerary.

    Example:
        >>> details = generate_itinerary_request_from_model_with_tools("Create an itinerary for a summer vacation in Hawaii")
        >>> print(details)
    """

    # Create an instance of GenericAgent
    generic_agent = GenericAgent(model_name=model_name, pydantic_model=pydantic_model, tools=tools)

    append_this = "  Respond with final answer using ItineraryRequest output format and only the ItineraryRequest format."

    # Append the string
    prompt += append_this

    # Generate the response using the agent
    result = generic_agent.generate_response(prompt)

    return result
