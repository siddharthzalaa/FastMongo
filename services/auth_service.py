from utils.auth_utils import verify_password, create_access_token
from database.connection import get_db

def login_user(user, db):
    user_collection = db["users"]

    db_user = user_collection.find_one({"email": user.email})

    if not db_user:
        return {"error": "User not found"}

    if not verify_password(user.password, db_user["password"]):
        return {"error": "Invalid password"}

    token = create_access_token({
        "email": db_user["email"],   # 👈 IMPORTANT (matches verify_token)
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