from pydantic import BaseModel, field_validator
from typing import List


class Department(BaseModel):
    id: str
    name: str

    @field_validator("name")
    def validate_name(cls, value):
        if value is None or value.strip() == "":
            raise ValueError("Department name cannot be empty")
        return value


class DepartmentPagination(BaseModel):
    data: List[Department]
    total: int
    page: int
    limit: int


def department_helper(dept: dict) -> dict:
    return {
        "id": str(dept["_id"]),   # direct access (safe)
        "name": dept["name"]      # enforce required field
    }