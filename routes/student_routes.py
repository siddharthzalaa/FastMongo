from typing import List

from fastapi import APIRouter, HTTPException
from database.connection import student_collection, department_collection
from schemas.student_schema import StudentCreate, StudentOut
from services.counter_service import get_next_student_id
from services.student_service import student_helper

router = APIRouter(tags=["students"])

@router.post("/add_student")
def add_student(student: StudentCreate):
    try:
        data = student.model_dump()

        dept = department_collection.find_one({"dept_id": data["department_id"]})
        if not dept:
            raise HTTPException(status_code=404, detail="Invalid Department")

        data["student_id"] = get_next_student_id()

        result = student_collection.insert_one(data)

        return {
            "id": str(result.inserted_id),
            "student_id": data["student_id"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_students", response_model=List[StudentOut])
def get_students():
    try:
        result = list(student_collection.find())

        return [student_helper(student) for student in result]

        return result
    except Exception as e:
        return {"error": str(e)}

@router.get("/get_student_by_id/{student_id}", response_model=StudentOut)
def get_students_by_id(student_id: int):
    try:
        student = student_collection.find_one({"student_id" : student_id})
        if not student:
            return HTTPException(status_code=404, detail="Student not found")

        return student_helper(student)

    except Exception as e:
        return {"error": str(e)}


@router.get("",response_model=List[StudentOut])
def get_students_by_department(department_id: int):
    try:
        students = list(student_collection.aggregate([
            {
                "$match": {"department_id": department_id}
            },
            {
                "$lookup": {
                    "from": "department",
                    "localField": "department_id",
                    "foreignField": "deptId",
                    "as": "department_details"
                }
            },
            {
                "$unwind": "$department_details"
            }
        ]))

        if not students:
            return HTTPException(status_code=404, detail="Student not found")

        return [student_helper(student) for student in students]

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete_student_by_id/{student_id}")
def delete_student(student_id: int):
    try:
        result = student_collection.delete_one({"student_id" : student_id})

        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Student not found")

        return {
            "student_id": student_id,
            "deleted" : True
        }
    except Exception as e:
        return {"error": str(e)}