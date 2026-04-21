from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends, Query

from database.connection import get_db
from schemas.student_schema import StudentCreate, StudentOut, StudentPagination
from services.counter_service import get_next_student_id
from services.pagination_service import paginate
from services.student_service import student_helper

router = APIRouter(tags=["students"])

@router.post("/add_student")
def add_student(student: StudentCreate, db=Depends(get_db)):
    try:
        data = student.model_dump()

        student_collection = db["students"]
        department_collection = db["department"]

        print("DATA:", data)

        dept = department_collection.find_one({"deptId": data["department_id"]})
        if not dept:
            raise HTTPException(status_code=404, detail="Invalid Department")

        data["student_id"] = get_next_student_id(db)

        result = student_collection.insert_one(data)

        return {
            "id": str(result.inserted_id),
            "student_id": data["student_id"]
        }

    except HTTPException as e:
        print("HTTP ERROR:", repr(e))
        raise


@router.get("/get_students", response_model=StudentPagination)
def get_students(
        page: int = Query(1, ge=1),
        limit : int = Query(10, ge=1, le=100),
        db = Depends(get_db)):
    try:
        student_collection = db["students"]

        result = paginate(student_collection, page, limit)

        result["data"] = [student_helper(student) for student in result["data"]]

        return result

    except Exception as e:
        return {"error": str(e)}

@router.get("/get_student_by_id/{student_id}", response_model=StudentOut)
def get_students_by_id(student_id: int, db = Depends(get_db)):
    try:
        student_collection = db["students"]
        student = student_collection.find_one({"student_id" : student_id})
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        return student_helper(student)

    except Exception as e:
        return {"error": str(e)}


@router.get("",response_model=List[StudentOut])
def get_students_by_department(department_id: int, db = Depends(get_db)):
    try:
        student_collection = db["students"]
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
def delete_student(student_id: int,db = Depends(get_db)):
    try:
        student_collection = db["students"]
        result = student_collection.delete_one({"student_id" : student_id})

        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Student not found")

        return {
            "student_id": student_id,
            "deleted" : True
        }
    except Exception as e:
        return {"error": str(e)}