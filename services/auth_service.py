from fastapi import HTTPException

from utils.auth_utils import verify_password, create_access_token
from database.connection import get_db
from utils.logger_utils import logger


def login_user(user, db):
    user_collection = db["users"]

    db_user = user_collection.find_one({"email": user.email})

    if not db_user:
        logger.warning(f"User with email {user.email} does not exist")
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(user.password, db_user["password"]):
        logger.warning(f"User with email {user.email} has incorrect password")
        raise HTTPException(status_code=401, detail="Invalid password")

    token = create_access_token({
        "email": db_user["email"],
        "role": db_user["role"]
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }

    return {
        "access_token": token,
        "token_type": "bearer"
    }