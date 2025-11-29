from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.repositories.task_repository import TaskRepository
from app.repositories.project_repository import ProjectRepository
from app.services.task_service import TaskService, TaskNotFound, ValidationError
from app.schemas.task_schema import TaskCreate, TaskUpdate, TaskOut

router = APIRouter(prefix="/projects/{project_id}/tasks", tags=["tasks"])


def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    task_repo = TaskRepository(db)
    project_repo = ProjectRepository(db)
    return TaskService(task_repo, project_repo)


@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(
    project_id: int,
    data: TaskCreate,
    service: TaskService = Depends(get_task_service),
):
    try:
        return service.add_task(project_id, data.title, data.description or "", data.deadline)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[TaskOut])
def list_tasks(project_id: int, service: TaskService = Depends(get_task_service)):
    return service.list_tasks_by_project(project_id)


@router.get("/{task_id}", response_model=TaskOut)
def get_task(project_id: int, task_id: int, service: TaskService = Depends(get_task_service)):
    try:
        task = service.get_task(task_id)
        # (اختیاری) چک تعلق به پروژه
        if task.project_id != project_id:
            raise TaskNotFound("Task not found in this project")
        return task
    except TaskNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{task_id}", response_model=TaskOut)
def update_task(
    project_id: int,
    task_id: int,
    data: TaskUpdate,
    service: TaskService = Depends(get_task_service),
):
    try:
        return service.update_task(task_id, data.model_dump(exclude_unset=True))
    except TaskNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{task_id}/status", response_model=TaskOut)
def change_status(
    project_id: int,
    task_id: int,
    status_value: str,
    service: TaskService = Depends(get_task_service),
):
    try:
        return service.change_status(task_id, status_value)
    except TaskNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(project_id: int, task_id: int, service: TaskService = Depends(get_task_service)):
    try:
        service.delete_task(task_id)
    except TaskNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))