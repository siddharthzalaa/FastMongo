from fastapi import APIRouter, HTTPException, Depends
from fastapi.params import Query

from database.connection import get_db
from schemas.department_schema import Department, DepartmentPagination, department_helper
from services.counter_service import get_next_department_id
from services.pagination_service import paginate
from utils.auth_utils import verify_token, user_or_admin, admin_only
from utils.logger_utils import logger

router = APIRouter(tags=["departments"])

@router.get("/get_departments", response_model=DepartmentPagination)
def get_departments(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str = Query(None),
    db=Depends(get_db),
    user=Depends(user_or_admin)
):
    department_collection = db["department"]

    filter_query = {}

    if search:
        filter_query["name"] = {"$regex": search, "$options": "i"}

    result = paginate(department_collection, page, limit, filter_query)

    result["data"] = [department_helper(dept) for dept in result["data"]]

    return result

@router.post("/create_department")
def create_department(department: Department, db = Depends(get_db),
        user= Depends(admin_only)):
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
        logger.error(f"Error in creating department: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete_department_by_id/{department_id}")
def delete_department(department_id: int, db = Depends(get_db),
        user= Depends(admin_only)):
    try:
        department_collection = db["department"]
        department = department_collection.find_one({"deptId" : department_id})

        if not department:
            raise HTTPException(status_code=404, detail="Department not found")
        else:
            department_collection.delete_one({"deptId" : department_id})
            return {"department_id": department_id,
                    "deleted": True}
    except Exception as e:
        logger.error(f"Error in deleting department: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
