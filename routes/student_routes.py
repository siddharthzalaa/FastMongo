from fastapi import APIRouter
from database.connection import student_collection
from schemas.student_schema import Student
from services.counter_service import get_next_student_id

router = APIRouter(tags=["students"])

@router.post("/create_student")
def create_student(student: Student):
    try:
        data = student.model_dump()

        data["student_id"] = get_next_student_id()

        result = student_collection.insert_one(data)

        return {
            "id": str(result.inserted_id),
            "student_id": data["student_id"]
        }

    except Exception as e:
        return {"error": str(e)}

@router.get("/get_students")
def get_students():
    try:
        result = list(student_collection.find())

        for student in result:
            student["_id"] = str(student["_id"])

        return result
    except Exception as e:
        return {"error": str(e)}

@router.get("/get_students_by_id")
def get_students_by_id(student_id: int):
    try:
        student = student_collection.find_one({"student_id" : student_id})
        if not student:
            return {"error": "Student not found"}

        student["_id"] = str(student["_id"])

        return student
    except Exception as e:
        return {"error": str(e)}

@router.delete("/delete_student_by_id")
def delete_student(student_id: int):
    try:
        student = student_collection.find_one({"student_id" : student_id})

        if not student:
            return {"error": "Student not found"}
        else:
            student_collection.delete_one({"student_id" : student_id})
            return {"student_id": student_id,
                    "deleted": True}
    except Exception as e:
        return {"error": str(e)}