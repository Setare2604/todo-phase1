from fastapi import FastAPI
from app.controllers.project_controller import router as project_router
from app.controllers.task_controller import router as task_router

app = FastAPI(title="ToDoList Web API", version="3.0.0")

app.include_router(project_router)
app.include_router(task_router)


@app.get("/")
def root():
    return {"status": "ok", "message": "ToDoList API is running"}