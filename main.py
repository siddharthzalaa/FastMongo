from fastapi import FastAPI
from starlette.responses import RedirectResponse

from routes.department_routes import router as department_routes
from routes.student_routes import router as student_routes

from middleware.logging import log_requests

app = FastAPI()

app.middleware("http")(log_requests)

@app.get("/")
def redirect_to_docs():
    return RedirectResponse(url="/docs#")


app.include_router(student_routes, prefix="/students", tags=["students"])
app.include_router(department_routes, prefix="/departments", tags=["departments"])

