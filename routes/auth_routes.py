from fastapi import APIRouter
from fastapi.params import Depends

from database.connection import get_db
from schemas.auth_schema import LoginSchema
from services.auth_service import login_user

router = APIRouter(tags=["auth"])

@router.post("/login")
def login(user: LoginSchema, db=Depends(get_db)):
    return login_user(user,db)