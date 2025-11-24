from typing import List, Optional
from app.repositories.project_repository import ProjectRepository
from app.models.project import Project
from datetime import datetime

class ProjectNotFound(Exception):
    pass

class ValidationError(Exception):
    pass

class ProjectService:
    def __init__(self, project_repo: ProjectRepository):
        self.project_repo = project_repo

    def create_project(self, name: str, description: str = "") -> Project:
        name = name.strip()
        if not (1 <= len(name) <= 100):
            raise ValidationError("Project name must be 1..100 characters")

        # uniqueness check (repository provides get_by_name)
        if self.project_repo.get_by_name(name) is not None:
            raise ValidationError("Project with this name already exists")

        return self.project_repo.create(name=name, description=description)

    def get_project(self, project_id: int) -> Project:
        proj = self.project_repo.get(project_id)
        if proj is None:
            raise ProjectNotFound(f"Project {project_id} not found")
        return proj

    def list_projects(self) -> List[Project]:
        return self.project_repo.list()

    def delete_project(self, project_id: int) -> None:
        proj = self.project_repo.get(project_id)
        if proj is None:
            raise ProjectNotFound(f"Project {project_id} not found")
        self.project_repo.delete(project_id)