from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.repositories.project_repository import ProjectRepository
from app.services.project_service import ProjectService, ProjectNotFound, ValidationError
from app.schemas.project_schema import ProjectCreate, ProjectUpdate, ProjectOut

router = APIRouter(prefix="/projects", tags=["projects"])


def get_project_service(db: Session = Depends(get_db)) -> ProjectService:
    repo = ProjectRepository(db)
    return ProjectService(repo)


@router.post("/", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(
    data: ProjectCreate,
    service: ProjectService = Depends(get_project_service),
):
    try:
        return service.create_project(data.name, data.description or "")
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[ProjectOut])
def list_projects(service: ProjectService = Depends(get_project_service)):
    return service.list_projects()


@router.get("/{project_id}", response_model=ProjectOut)
def get_project(project_id: int, service: ProjectService = Depends(get_project_service)):
    try:
        return service.get_project(project_id)
    except ProjectNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{project_id}", response_model=ProjectOut)
def update_project(
    project_id: int,
    data: ProjectUpdate,
    service: ProjectService = Depends(get_project_service),
):
    try:
        return service.update_project(project_id, data.model_dump(exclude_unset=True))
    except ProjectNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, service: ProjectService = Depends(get_project_service)):
    try:
        service.delete_project(project_id)
    except ProjectNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))