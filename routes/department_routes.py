from fastapi import APIRouter, HTTPException, Depends

from database.connection import get_db
from schemas.department_schema import Department
from services.counter_service import get_next_department_id

router = APIRouter(tags=["departments"])

@router.get("/get_departments")
def get_department(db = Depends(get_db)):
        try:
            department_collection = db["department"]
            results = list(department_collection.find())

            for department in results:
                department["_id"] = str(department["_id"])

            return results

        except Exception as e:
            return {"error": str(e)}

@router.post("/create_department")
def create_department(department: Department, db = Depends(get_db)):
    try:

        data = department.model_dump()
        department_collection = db["department"]
        department_exist=department_collection.find_one({"name":data["name"]})

        if department_exist:
            raise HTTPException(
                status_code=400,
                detail="Department already exists"
            )

        data["deptId"] = get_next_department_id(db)

        result = department_collection.insert_one(data)

        return {
            "id": str(result.inserted_id),
            "department_id": data["deptId"]
        }

    except Exception as e:
        return {"error": str(e)}

@router.delete("/delete_department_by_id/{department_id}")
def delete_student(department_id: int, db = Depends(get_db)):
    try:
        department_collection = db["department"]
        department = department_collection.find_one({"deptId" : department_id})

        if not department:
            return {"error": "Department not found"}
        else:
            department_collection.delete_one({"student_id" : department_id})
            return {"department_id": department_id,
                    "deleted": True}
    except Exception as e:
        return {"error": str(e)}
