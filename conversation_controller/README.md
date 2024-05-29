# Conversation Controller

## Overview
This package contains the `ConversationController` class, designed to help create and manage travel plans interactively. It guides the user through a series of inputs to gather necessary details about events, location, and dates of a trip before creating a summarized itinerary.

## Usage
To use the ConversationController in your project, you can import and initialize it as follows:
```
from my_travel_planner import TravelPlansController

controller = TravelPlansController()
start_point = input("Please choose a starting point (activity, destination, dates): ")
controller.start(start_point)

```




### Create an Itinerary by passing in values directly
```
from travel_plans_controller import TravelPlansController

def main():

controller = TravelPlansController()

    # Padded values for the state, replace these with appropriate example data
    controller.state['activities'] = "museum visit, beach"
    controller.state['destination'] = "Barcelona"
    controller.state['dates'] = "2024-06-01 to 2024-06-15"

    # Directly jump to the last step which creates the itinerary
    controller.jump_to_last_step()

if __name__ == "__main__":
main()
```
