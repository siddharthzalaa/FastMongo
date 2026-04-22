
import time
import uuid
from datetime import datetime

from fastapi import Request
from jose import jwt, JWTError
import os

from utils.logger_utils import logger

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())[:8]
    start_time = time.time()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    query_params = request.query_params
    client_ip = request.client.host if request.client.host else 'Unknown'

    user_email = "anonymous"

    auth_header = request.headers.get("authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_email = payload.get("sub", "unknown")
        except JWTError:
            user_email = "invalid_token"

    response = await call_next(request)

    end_time = time.time()
    process_time = end_time - start_time

    logger.info(
        f"ID: {request_id} | "
        f"User: {user_email} | "
        f"IP: {client_ip} | "
        f"{request.method} {request.url.path} | "
        f"Status: {response.status_code} | "
        f"Time: {process_time:.4f}s"
    )

    return response