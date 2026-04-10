from pydantic import BaseModel, field_validator
from typing import List, Dict

class Department(BaseModel):
    name: str

    @field_validator("name")
    def validate_name(cls, value):
        if value is None or value.strip() == "":
            raise ValueError("Department name cannot be empty")
        return value