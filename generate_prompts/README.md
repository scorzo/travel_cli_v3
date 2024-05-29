# Generate Prompts Package

## Overview
The `generate_prompts` package provides utilities to manage and generate lists of prompts with metadata. It includes Pydantic models for structured data handling.

## Installation
Download the package and include it in your Python project directory.

## Usage
Import the `Prompt` and `PromptsList` classes from the package to create and manipulate lists of prompts:

```python
from generate_prompts.generator import generate_prompts_from_model
import json

test_prompt = "Generate 3 travel itinerary prompts"

    # Call the function and capture the output
    output = generate_prompts_from_model(test_prompt)

    # Print the output to verify it's working as expected
    print("Generated Prompts:")
    print(json.dumps(output, indent=2))
    
    # Generated Prompts:
    {
      "prompts": [
        {
          "text": "Create a 7-day travel itinerary for a family vacation in Paris, including activities for children and dining recommendations."
        },
        {
          "text": "Design a 10-day adventure travel itinerary in New Zealand, focusing on outdoor activities like hiking, bungee jumping, and kayaking."
        },
        {
          "text": "Plan a 5-day cultural and historical travel itinerary in Kyoto, Japan, including visits to temples, traditional tea houses, and local markets."
        }
      ],
      "created_at": "2023-10-02",
      "description": "A collection of travel itinerary prompts for various destinations and interests."
    }
