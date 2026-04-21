from pydantic import BaseModel
from typing import List, Dict, Optional

from schemas.department_schema import Department


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
    department_id: int

class StudentOut(BaseModel):
    id: str
    name: str
    age: int
    hobbies: List[str]
    bio: str
    identity: Optional[Identity] = None
    experience: Optional[List[Experience]] = None
    student_id: Optional[int] = None
    department_id: Optional[int] = None