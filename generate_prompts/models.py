from langchain_core.pydantic_v1 import BaseModel, validator
from typing import List
from datetime import datetime, date

class Prompt(BaseModel):
    text: str

class PromptsList(BaseModel):
    prompts: List[Prompt]
    created_at: date
    description: str

