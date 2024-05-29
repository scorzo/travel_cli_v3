from .conversation_controller import ConversationController
from itinerary_package.generator import generate_itinerary_from_model_with_tools

class TravelPlansController(ConversationController):
    def __init__(self, persona_description=None):
        steps = [self.collect_activities, self.collect_destination, self.collect_dates, self.collect_adults, self.collect_children, self.create_itinerary]
        state = {
            'activities': None,
            'destination': None,
            'dates': None,
            'adults': None,
            'children': None,
            'itinerary': None
        }
        descriptions = {
            'activities': "Please enter the activities you're interested in (e.g., concert, museum visit): ",
            'destination': "Please enter the destination of your trip: ",
            'dates': "Please enter the dates of your trip (e.g., YYYY-MM-DD to YYYY-MM-DD): ",
            'adults': "Please enter the number of adults: ",
            'children': "Please enter the number of children: ",
            'itinerary': ""
        }
        entry_points = {
            'activities': 0,
            'destination': 1,
            'dates': 2,
            'adults': 3,
            'children': 4
        }
        super().__init__(steps, state, descriptions, entry_points, persona_description)

    def collect_activities(self, human_input):
        self.state['activities'] = human_input
        print(f"Activities collected: {human_input}")

    def collect_destination(self, human_input):
        self.state['destination'] = human_input
        print(f"Destination collected: {human_input}")

    def collect_dates(self, human_input):
        self.state['dates'] = human_input
        print(f"Dates collected: {human_input}")

    def collect_adults(self, human_input):
        self.state['adults'] = human_input
        print(f"Number of adults collected: {human_input}")

    def collect_children(self, human_input):
        self.state['children'] = human_input
        print(f"Number of children collected: {human_input}")

    def create_itinerary(self, human_input):
        components = []
        if self.state['destination']:
            components.append(f"a trip to {self.state['destination']}")
        if self.state['dates']:
            components.append(f"from {self.state['dates']}")
        if self.state['activities']:
            components.append(f"including activities such as {self.state['activities']}")
        if self.state['adults']:
            components.append(f"with {self.state['adults']} adults")
        if self.state['children']:
            components.append(f"and {self.state['children']} children")

        if components:
            description = "Create an itinerary for " + ', '.join(components) + "."
        else:
            description = "Create a general itinerary."

        itinerary_details = generate_itinerary_from_model_with_tools(description)
        self.state['itinerary'] = itinerary_details
        print(f"Final Itinerary: {itinerary_details}")
