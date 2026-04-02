from pydantic import BaseModel
from typing import List, Dict

class Experience(BaseModel):
    company: str
    duration: float

class Identity(BaseModel):
    hasPanCard: bool
    hasAdhaarCard: bool

class Student(BaseModel):
    name: str
    age: int
    Hobbies: List[str]
    bio: str
    identity: Identity
    experience: List[Experience]