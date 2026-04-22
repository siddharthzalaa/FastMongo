from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends, Query

from database.connection import get_db
from schemas.student_schema import StudentCreate, StudentOut, StudentPagination
from services.counter_service import get_next_student_id
from services.pagination_service import paginate
from services.student_service import student_helper
from utils.auth_utils import verify_token, admin_only, user_or_admin
from utils.logger_utils import logger

router = APIRouter(tags=["students"])

@router.post("/add_student")
def create_student(student: StudentCreate, db=Depends(get_db),
        user= Depends(admin_only)):
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
        logger.error(f"Error in adding student: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get_students", response_model=StudentPagination)
def get_students(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    department_id: int = Query(None),
    age: int = Query(None),
    search: str = Query(None),
    db=Depends(get_db),
    user=Depends(user_or_admin)
):
    student_collection = db["students"]

    filter_query = {}

    if department_id:
        filter_query["department_id"] = department_id

    if age:
        filter_query["age"] = age

    if search:
        filter_query["name"] = {"$regex": search, "$options": "i"}

    result = paginate(student_collection, page, limit, filter_query)

    result["data"] = [student_helper(student) for student in result["data"]]

    return result

@router.get("/get_student_by_id/{student_id}", response_model=StudentOut)
def get_students_by_id(student_id: int, db = Depends(get_db)):

        student_collection = db["students"]
        student = student_collection.find_one({"student_id" : student_id})
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        return student_helper(student)

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
        logger.error(f"Error in getting students: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete_student_by_id/{student_id}")
def delete_student(student_id: int,db = Depends(get_db),
        user= Depends(admin_only)):
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
        logger.error(f"Error in deleting student: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))