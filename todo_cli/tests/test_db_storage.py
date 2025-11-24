from todo_cli.storage.db_storage import DBStorage
from todo_cli.core.models import Project as DomainProject, Task as DomainTask, TaskStatus
from app.db.session import SessionLocal

def test_db_storage_create_project_and_task():
    # NOTE: DBStorage in your implementation uses SessionLocal which points to real DB.
    # For unit tests override DBStorage to accept a session or inject test session.
    # Below is a simplified approach assuming DBStorage accepts session param (recommended).
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from app.db.base import Base

    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=False, future=True)
    session = Session()

    # If your DBStorage has constructor DBStorage(session=None)
    storage = DBStorage(session=session)

    p = DomainProject(0, "SProj", "sd")
    created = storage.create_project(p)
    assert created.project_id > 0
    assert created.name == "SProj"

    t = DomainTask(0, created.project_id, "TTitle", "desc")
    created_task = storage.create_task(t)
    assert created_task.task_id > 0
    assert created_task.project_id == created.project_id