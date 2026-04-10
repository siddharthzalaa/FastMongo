from fastapi import APIRouter, HTTPException

from database.connection import department_collection
from schemas.department_schema import Department
from services.counter_service import get_next_department_id

router = APIRouter(tags=["departments"])

@router.get("/get_departments")
def get_department():
        try:
            results = list(department_collection.find())

            for department in results:
                department["_id"] = str(department["_id"])

            return results

        except Exception as e:
            return {"error": str(e)}

@router.post("/create_department")
def create_department(department: Department):
    try:

        data = department.model_dump()

        department_exist=department_collection.find_one({"name":data["name"]})

        if department_exist:
            raise HTTPException(
                status_code=400,
                detail="Department already exists"
            )

        data["deptId"] = get_next_department_id()

        result = department_collection.insert_one(data)

        return {
            "id": str(result.inserted_id),
            "department_id": data["deptId"]
        }

    except Exception as e:
        return {"error": str(e)}

@router.delete("/delete_department_by_id/{department_id}")
def delete_student(department_id: int):
    try:
        student = department_collection.find_one({"student_id" : department_id})

        if not student:
            return {"error": "Student not found"}
        else:
            department_collection.delete_one({"student_id" : department_id})
            return {"department_id": department_id,
                    "deleted": True}
    except Exception as e:
        return {"error": str(e)}
