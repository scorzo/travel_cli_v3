# Prompt Converter Package

The Prompt Converter package converts prompts to the voice of a specified AI persona and generates concise response suggestions based on user preferences.

## Example Usage

```python
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

print(json.dumps(converted_prompt, indent=2))
print(json.dumps(response_suggestions, indent=2))
