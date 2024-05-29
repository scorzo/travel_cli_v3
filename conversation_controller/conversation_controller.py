from ai_voice import PromptConverter

class ConversationController:
    def __init__(self, steps, state, descriptions, entry_points=None, persona_description=None):
        self.steps = steps
        self.state = state
        self.descriptions = descriptions
        self.current_step = 0
        self.entry_points = entry_points or {}
        self.persona_description = persona_description

    def start(self, entry_point):
        if entry_point in self.entry_points:
            self.current_step = self.entry_points[entry_point]
        else:
            raise ValueError(f"Invalid entry point: {entry_point}")
        steps_completed = 0
        while steps_completed < len(self.steps) - 1:
            self.process_step()
            steps_completed += 1
            self.current_step = (self.current_step + 1) % (len(self.steps) - 1)
        self.steps[-1](None)  # Assume the last step handles finalization

    def process_step(self):
        step_function = self.steps[self.current_step]
        description = self.descriptions[step_function.__name__.split('_')[1]]

        if self.persona_description:
            converter = PromptConverter(self.persona_description, newline_after_prompt=True, convert_prompt_flag=False)
            converted_description = converter.convert_prompt(description)
            prompt = converted_description['converted_prompt']
        else:
            prompt = description

        user_input = input(prompt)
        step_function(user_input)


    def jump_to_last_step(self):
        # Set the current step to the last step in the list
        self.current_step = len(self.steps) - 1
        # Execute the last step with no input (or appropriate input if necessary)
        self.steps[self.current_step](None)  # Adjust this if the last step needs specific input

        print("Jumped to and executed the last step.")
