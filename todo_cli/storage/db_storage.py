from typing import Optional, List
from app.db.session import SessionLocal
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from todo_cli.core.models import Project as DomainProject, Task as DomainTask, TaskStatus

class DBStorage:
    def __init__(self):
        self.db = SessionLocal()

    # Projects
    def create_project(self, domain_project: DomainProject) -> DomainProject:
        repo = ProjectRepository(self.db)
        p = repo.create(name=domain_project.name, description=domain_project.description)
        # map ORM -> Domain
        return DomainProject(p.id, p.name, p.description)

    def get_all_projects(self) -> List[DomainProject]:
        repo = ProjectRepository(self.db)
        res = []
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
        # fetch model, update fields then commit via repository
        p = repo.get(domain_project.project_id)
        if not p:
            return False
        p.name = domain_project.name
        p.description = domain_project.description
        self.db.commit()
        return True

    def delete_project(self, project_id: int) -> bool:
        repo = ProjectRepository(self.db)
        repo.delete(project_id)
        return True

    # Tasks - similar mapping
    def create_task(self, domain_task: DomainTask) -> DomainTask:
        repo = TaskRepository(self.db)
        t = repo.create(project_id=domain_task.project_id, title=domain_task.title,
                        description=domain_task.description, deadline=domain_task.deadline)
        return DomainTask(t.id, t.project_id, t.title, t.description, TaskStatus(t.status), t.deadline)

    def get_tasks_by_project_id(self, project_id: int):
        repo = TaskRepository(self.db)
        tasks = repo.list_by_project(project_id)
        return [DomainTask(t.id, t.project_id, t.title, t.description, TaskStatus(t.status), t.deadline) for t in tasks]

    def get_task_by_id(self, task_id: int):
        repo = TaskRepository(self.db)
        t = repo.get(task_id)
        if not t:
            return None
        return DomainTask(t.id, t.project_id, t.title, t.description, TaskStatus(t.status), t.deadline)

    def update_task(self, domain_task: DomainTask) -> bool:
        repo = TaskRepository(self.db)
        t = repo.get(domain_task.task_id)
        if not t:
            return False
        t.title = domain_task.title
        t.description = domain_task.description
        t.status = domain_task.status.value
        t.deadline = domain_task.deadline
        self.db.commit()
        return True

    def delete_task(self, task_id: int) -> bool:
        repo = TaskRepository(self.db)
        return repo.delete(task_id)