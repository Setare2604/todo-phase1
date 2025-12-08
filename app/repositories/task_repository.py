from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.task import Task, StatusEnum
from datetime import datetime

class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, project_id: int, title: str, description: str = "", deadline=None) -> Task:
        t = Task(project_id=project_id, title=title, description=description, deadline=deadline)
        self.db.add(t)
        self.db.commit()
        self.db.refresh(t)
        return t

    def get(self, task_id: int) -> Optional[Task]:
        return self.db.query(Task).filter(Task.id == task_id).first()

    def list_by_project(self, project_id: int) -> List[Task]:
        return self.db.query(Task).filter(Task.project_id == project_id).all()

    def change_status(self, task_id: int, new_status: StatusEnum) -> Optional[Task]:
        t = self.get(task_id)
        if not t:
            return None

        t.status = new_status


        if new_status == StatusEnum.DONE:
            t.closed_at = datetime.utcnow()
        else:
            t.closed_at = None

        self.db.commit()
        self.db.refresh(t)
        return t


    def update(self, task: Task) -> bool:
        if not self.get(task.id):
            return False
        self.db.merge(task)
        self.db.commit()
        return True

    def delete(self, task_id: int) -> bool:
        t = self.get(task_id)
        if not t:
            return False
        self.db.delete(t)
        self.db.commit()
        return True
    def list_overdue_open_tasks(self) -> List[Task]:
        now = datetime.utcnow()
        return (
            self.db.query(Task)
            .filter(Task.deadline.isnot(None))
            .filter(Task.deadline < now)
            .filter(Task.status != StatusEnum.DONE)
            .all()
        )