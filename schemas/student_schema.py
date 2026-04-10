from pydantic import BaseModel
from typing import List, Dict, Optional


class Experience(BaseModel):
    company: str
    duration: float

class Identity(BaseModel):
    hasPanCard: bool
    hasAdhaarCard: bool

class StudentCreate(BaseModel):
    name: str
    age: int
    Hobbies: List[str]
    bio: str
    identity: Identity
    experience: List[Experience]

class StudentOut(BaseModel):
    id: str
    name: str
    age: int
    hobbies: List[str]
    bio: str
    identity: Optional[Identity] = None
    experience: Optional[List[Experience]] = None
    student_id: int
    department_id: int