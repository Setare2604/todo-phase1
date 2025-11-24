from typing import Optional, List
from app.db.session import SessionLocal
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from todo_cli.core.models import Project as DomainProject, Task as DomainTask, TaskStatus
from datetime import datetime

class DBStorage:
    def __init__(self):
        # یک session یک‌بار ساخته می‌شود و تا زمان بسته شدن نگه‌داری می‌گردد
        self.db = SessionLocal()

    def close(self):
        """Close DB session (call when shutting down/tests)"""
        try:
            self.db.close()
        except Exception:
            pass

    # -------------------
    # Projects
    # -------------------
    def create_project(self, domain_project: DomainProject) -> DomainProject:
        repo = ProjectRepository(self.db)
        p = repo.create(name=domain_project.name, description=domain_project.description)
        # map ORM -> Domain (اگر ORM فیلد created_at داشت از آن استفاده کن)
        created_at = getattr(p, "created_at", None) or datetime.now()
        return DomainProject(p.id, p.name, p.description)

    def get_all_projects(self) -> List[DomainProject]:
        repo = ProjectRepository(self.db)
        res: List[DomainProject] = []
        for p in repo.list():
            res.append(DomainProject(p.id, p.name, p.description))
        return res

    def get_project_by_id(self, project_id: int) -> Optional[DomainProject]:
        repo = ProjectRepository(self.db)
        p = repo.get(project_id)
        if not p:
            return None
        return DomainProject(p.id, p.name, p.description)

    def update_project(self, domain_project: DomainProject) -> bool:
        repo = ProjectRepository(self.db)
        p = repo.get(domain_project.project_id)
        if not p:
            return False
        p.name = domain_project.name
        p.description = domain_project.description
        self.db.commit()
        return True

    def delete_project(self, project_id: int) -> bool:
        repo = ProjectRepository(self.db)
        return repo.delete(project_id)

    # -------------------
    # Tasks
    # -------------------
    def create_task(self, domain_task: DomainTask) -> DomainTask:
        repo = TaskRepository(self.db)
        t = repo.create(
            project_id=domain_task.project_id,
            title=domain_task.title,
            description=domain_task.description,
            deadline=domain_task.deadline
        )

        # robust mapping for status (handle if t.status is Enum or str)
        status_value = None
        if hasattr(t, "status"):
            status_attr = t.status
            # if it's an enum with .value
            status_value = getattr(status_attr, "value", None) or str(status_attr)

        # ensure we pass a TaskStatus instance to DomainTask
        try:
            status_enum = TaskStatus(status_value) if status_value is not None else TaskStatus.TODO
        except Exception:
            # fallback safe
            status_enum = TaskStatus.TODO

        created_at = getattr(t, "created_at", None) or datetime.now()

        return DomainTask(t.id, t.project_id, t.title, t.description, status_enum, t.deadline)

    def get_tasks_by_project_id(self, project_id: int) -> List[DomainTask]:
        repo = TaskRepository(self.db)
        tasks = repo.list_by_project(project_id)
        result: List[DomainTask] = []

        for t in tasks:
            status_attr = getattr(t, "status", None)
            status_value = getattr(status_attr, "value", None) or (str(status_attr) if status_attr is not None else None)
            try:
                status_enum = TaskStatus(status_value) if status_value is not None else TaskStatus.TODO
            except Exception:
                status_enum = TaskStatus.TODO

            created_at = getattr(t, "created_at", None) or datetime.now()
            result.append(DomainTask(t.id, t.project_id, t.title, t.description, status_enum, t.deadline))

        return result

    def get_task_by_id(self, task_id: int) -> Optional[DomainTask]:
        repo = TaskRepository(self.db)
        t = repo.get(task_id)
        if not t:
            return None

        status_attr = getattr(t, "status", None)
        status_value = getattr(status_attr, "value", None) or (str(status_attr) if status_attr is not None else None)
        try:
            status_enum = TaskStatus(status_value) if status_value is not None else TaskStatus.TODO
        except Exception:
            status_enum = TaskStatus.TODO

        created_at = getattr(t, "created_at", None) or datetime.now()

        return DomainTask(t.id, t.project_id, t.title, t.description, status_enum, t.deadline)

    def update_task(self, domain_task: DomainTask) -> bool:
        repo = TaskRepository(self.db)
        t = repo.get(domain_task.task_id)
        if not t:
            return False
        t.title = domain_task.title
        t.description = domain_task.description
        # store enum value (string) to DB field
        if hasattr(domain_task.status, "value"):
            t.status = domain_task.status.value
        else:
            t.status = str(domain_task.status)
        t.deadline = domain_task.deadline
        self.db.commit()
        return True

    def delete_task(self, task_id: int) -> bool:
        repo = TaskRepository(self.db)
        return repo.delete(task_id)