from datetime import datetime
from sqlalchemy.orm import Session
from app.repositories.task_repository import TaskRepository
from app.models.task import StatusEnum

def autoclose_overdue_tasks(db: Session) -> int:
    """
    Finds all tasks with deadline < now and status != DONE
    and closes them. Returns number of closed tasks.
ردیف‌های overdue رو می‌بنده و تعدادش رو برمی‌گردونه.
    """
    repo = TaskRepository(db)
    overdue_tasks = repo.list_overdue_open_tasks()

    now = datetime.utcnow()
    for t in overdue_tasks:
        t.status = StatusEnum.DONE
        t.closed_at = now

    if overdue_tasks:
        db.commit()

    return len(overdue_tasks)