from fastapi import HTTPException

from services.counter_service import get_next_student_id
from services.pagination_service import paginate


def student_helper(student) -> dict:
    if not student:
        return {}

    return {
        "id": str(student.get("_id")),
        "name": student.get("name"),
        "age": student.get("age"),
        "hobbies": student.get("Hobbies", []),
        "bio": student.get("bio"),
        "identity": student.get("identity"),
        "experience": student.get("experience"),
        "student_id": student.get("student_id"),
        "department_id": student.get("department_id")
    }

def create_student(data: dict, db):
    student_collection = db["students"]
    department_collection = db["department"]

    dept = department_collection.find_one({"deptId": data["department_id"]})
    if not dept:
        raise HTTPException(status_code=404, detail="Invalid Department")

    data["student_id"] = get_next_student_id(db)

    result = student_collection.insert_one(data)

    return {
        "id": str(result.inserted_id),
        "student_id": data["student_id"]
    }

def get_students_service(db, page, limit, filter_query):
    student_collection = db["students"]

    result = paginate(student_collection, page, limit, filter_query)

    result["data"] = [student_helper(student) for student in result["data"]]

    return result

def get_student_by_id_service(student_id: int, db):
    student_collection = db["students"]

    student = student_collection.find_one({"student_id": student_id})

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student_helper(student)

def delete_student_service(student_id: int, db):
    student_collection = db["students"]

    result = student_collection.delete_one({"student_id": student_id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")

    return {
        "student_id": student_id,
        "deleted": True
    }