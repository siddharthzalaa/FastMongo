
import time
import uuid
from datetime import datetime

from fastapi import Request

async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())[:8]
    start_time = time.time()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    query_params = request.query_params
    client_ip = request.client.host if request.client.host else 'Unknown'
    response = await call_next(request)
    end_time = time.time()
    process_time = end_time - start_time

    print(
        f"[{timestamp}] | "
        f"ID: {request_id} | "
        f"IP: {client_ip} | "
        f"{request.method} {request.url.path} | "
        f"Query: {query_params} | "
        f"Status: {response.status_code} | "
        f"Time: {process_time:.4f}s"
    )

    return response