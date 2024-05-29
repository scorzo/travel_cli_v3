from langchain_core.pydantic_v1 import BaseModel
from typing import List, Optional
import json
from langchain_openai import ChatOpenAI

class ConvertedPrompt(BaseModel):
    original_prompt: str
    converted_prompt: str

class ResponseSuggestions(BaseModel):
    prompt: str
    response_suggestions: List[str]

class PromptConverter:
    def __init__(self, persona: str, model_name: str = "gpt-4", highlight_color: Optional[str] = '\033[93m', suggestions_color: Optional[str] = '\033[96m', newline_after_prompt: bool = False, convert_prompt_flag: bool = True):
        self.persona = persona
        self.model = ChatOpenAI(model=model_name, temperature=0)
        self.highlight_color = highlight_color
        self.suggestions_color = suggestions_color
        self.newline_after_prompt = newline_after_prompt
        self.convert_prompt_flag = convert_prompt_flag

    def convert_prompt(self, prompt: str) -> dict:
        if not self.convert_prompt_flag:
            return {'original_prompt': prompt, 'converted_prompt': prompt}

        enhanced_prompt = f"Rewrite the following prompt in {self.persona}: {prompt}"

        structured_llm = self.model.with_structured_output(ConvertedPrompt)
        response = structured_llm.invoke(enhanced_prompt)
        response_dict = response.dict()

        # Apply highlight color to the converted prompt
        if self.highlight_color:
            response_dict['converted_prompt'] = f"{self.highlight_color}{response_dict['converted_prompt']}\033[0m"

        if self.newline_after_prompt:
            response_dict['converted_prompt'] += "\n"

        return response_dict

    def generate_response_suggestions(self, prompt: str, personal_preferences: Optional[dict] = None) -> dict:
        suggestion_prompt = f"Provide three concise (1-3 words) response suggestions for the following prompt: '{prompt}'"
        if personal_preferences:
            suggestion_prompt += f" based on preferences {json.dumps(personal_preferences)}"

        structured_llm = self.model.with_structured_output(ResponseSuggestions)
        response = structured_llm.invoke(suggestion_prompt)
        response_dict = response.dict()

        # Apply suggestions color to each response suggestion
        if self.suggestions_color:
            response_dict['response_suggestions'] = [f"{self.suggestions_color}{suggestion}\033[0m" for suggestion in response_dict['response_suggestions']]

        return response_dict

# Example usage
if __name__ == "__main__":
    import sys
    import os
    # Add parent directory to sys.path
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    from dotenv import load_dotenv
    load_dotenv()

    json_file_path = "profiles/character_Alexandra_Hamilton_2024_04_17_v1.json"
    from digital_twin import JSONReader
    json_reader = JSONReader(json_file_path)

    try:
        personal_preferences = json_reader.read_json()
    except FileNotFoundError:
        personal_preferences = None

    persona_description = "The voice of Socrates, the Greek philosopher"
    prompt = "Please enter the activities you're interested in (e.g., concert, museum visit)"

    converter = PromptConverter(persona_description)
    converted_prompt = converter.convert_prompt(prompt)

    response_suggestions = converter.generate_response_suggestions(prompt, personal_preferences)

    print(converted_prompt['converted_prompt'])
    print(json.dumps(response_suggestions, indent=2))
