from typing import List, Optional
from datetime import datetime
from app.repositories.task_repository import TaskRepository
from app.repositories.project_repository import ProjectRepository
from app.models.task import Task, StatusEnum

class TaskNotFound(Exception):
    pass

class ValidationError(Exception):
    pass

class TaskService:
    def __init__(self, task_repo: TaskRepository, project_repo: ProjectRepository):
        self.task_repo = task_repo
        self.project_repo = project_repo

    def add_task(self, project_id: int, title: str, description: str = "", deadline: Optional[datetime] = None) -> Task:
        title = title.strip()
        if not (1 <= len(title) <= 100):
            raise ValidationError("Task title must be 1..100 characters")

        project = self.project_repo.get(project_id)
        if project is None:
            raise ValidationError("Project not found")

        return self.task_repo.create(project_id=project_id, title=title, description=description, deadline=deadline)

    def get_task(self, task_id: int) -> Task:
        t = self.task_repo.get(task_id)
        if t is None:
            raise TaskNotFound("Task not found")
        return t

    def list_tasks_by_project(self, project_id: int) -> List[Task]:
        return self.task_repo.list_by_project(project_id)

    def change_status(self, task_id: int, new_status: str) -> Task:
        # validate status
        try:
            status_enum = StatusEnum(new_status)
        except ValueError:
            raise ValidationError("Invalid status")

        task = self.task_repo.get(task_id)
        if task is None:
            raise TaskNotFound("Task not found")

        return self.task_repo.change_status(task_id, status_enum)