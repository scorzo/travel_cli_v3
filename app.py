from dotenv import load_dotenv
load_dotenv()

import sys
from conversation_controller.travel_plans_controller import TravelPlansController
from generate_prompts.generator import generate_prompts_from_model
from itinerary_package.generator import generate_itinerary_request_from_model_with_tools
from pprint import pprint
import json

from ai_voice import PromptConverter

persona_description = "The voice of Socrates, the Greek philosopher"
converter = PromptConverter(persona_description, convert_prompt_flag=False)

def main():

    welcome_prompt = "Welcome to the Travel Planner! Please follow the prompts to plan your itinerary."
    converted_welcome = converter.convert_prompt(welcome_prompt)
    print(converted_welcome['converted_prompt'])

    # Initialize the travel plans controller
    controller = TravelPlansController(persona_description)

    # Main menu loop
    while True:
        start_point = input("Choose a starting point (activities, destination, dates), type 'ideas' to start from suggested prompts, or type 'quit' to exit: ").lower()
        if start_point == 'quit':

            message = "Exiting Travel Planner. Thank you for using our service!"
            converted_message = converter.convert_prompt(message)
            print(converted_message['converted_prompt'])

            sys.exit(0)

        if start_point in ['activities', 'destination', 'dates']:
            try:
                controller.start(start_point)
                break
            except Exception as e:
                print(f"An error occurred: {e}")
        elif start_point == 'ideas':
            # Generate and list travel ideas

            # Path to the JSON file containing personal preferences
            json_file_path = "profiles/character_Alexandra_Hamilton_2024_04_17_v1.json"

            # Create an instance of JSONReader to read the JSON data
            from digital_twin import JSONReader
            json_reader = JSONReader(json_file_path)

            try:
                # Reading the JSON file to get personal preferences
                personal_preferences = json_reader.read_json()

                prompt = "Generate 10 single day outing ideas, each having 150 characters or less.  Include number of adults and children.  If children, make some events adult only and tailor those ideas accordingly.  Make the ideas as diverse as possible."

                # Generate prompts using the model with personal preferences
                output = generate_prompts_from_model(prompt, personal_preferences)

                # Print the generated prompts (assuming 'output' is print-friendly)
                json.dumps(output, indent=2)

            except Exception as e:
                print(f"An error occurred: {str(e)}")
                sys.exit(0)

            message = "Here are some Travel Ideas:"
            # if enabled, add voice to message
            converted_message = converter.convert_prompt(message)
            print(converted_message['converted_prompt'])

            for idx, prompt in enumerate(output['prompts'], 1):
                print(f"{idx}. {prompt['text']}")

            # Allow the user to select a travel idea
            choice = int(input("Select a travel idea by number: "))
            selected_prompt = output['prompts'][choice - 1]['text']

            # Generate an intermediate state object based on the selected prompt
            details = generate_itinerary_request_from_model_with_tools(selected_prompt)
            print("Intermediate State Object:")
            print(details)

            # Extract data from the details object
            start_date = details['start_date']
            end_date = details['end_date']
            dates = f"{start_date} to {end_date}"

            # Assuming destinations is a list of dictionaries, each containing a 'location' and a list of 'activities'
            destinations = details['destinations']

            # Extract number of adults and number of children
            number_of_adults = details['number_of_adults']
            number_of_children = details['number_of_children']

            # Format the destination string and activities
            destination_names = [destination['location'] for destination in destinations]
            activities = []
            for destination in destinations:
                for activity in destination['activities']:
                    activities.append(f"{activity['name']} in {destination['location']}")

            # Join the destinations and activities into strings
            destination_str = ", ".join(destination_names)
            activities_str = "; ".join(activities)

            # Initialize and set state for a new controller
            new_controller = TravelPlansController(persona_description)
            new_controller.state['activities'] = activities_str
            new_controller.state['destination'] = destination_str
            new_controller.state['dates'] = dates
            new_controller.state['adults'] = number_of_adults
            new_controller.state['children'] = number_of_children

            # Execute the last step to generate the itinerary
            new_controller.jump_to_last_step()

            # Display the final itinerary and break the loop
            message = "Final Itinerary from Suggested Prompts:"
            converted_message = converter.convert_prompt(message)
            print(converted_message['converted_prompt'])

            pprint(new_controller.state['itinerary'])
            break
        else:
            print("Invalid option. Please choose a valid starting point, type 'ideas' for suggested prompts, or type 'quit' to exit.")

    # Display the final itinerary (only for the original workflow)
    if start_point in ['activities', 'destination', 'dates']:

        message = "Final Itinerary:"
        converted_message = converter.convert_prompt(message)
        print(converted_message['converted_prompt'])

        pprint(controller.state['itinerary'])

if __name__ == "__main__":
    main()
