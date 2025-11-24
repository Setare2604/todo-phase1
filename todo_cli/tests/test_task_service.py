from datetime import datetime, timedelta
from app.models.task import StatusEnum

def test_task_create_and_list(task_repo, project_repo):
    p = project_repo.create(name="TP", description="d")
    t = task_repo.create(project_id=p.id, title="T1", description="d", deadline=None)
    assert t.id is not None
    assert t.title == "T1"

    tasks = task_repo.list_by_project(p.id)
    assert len(tasks) == 1

def test_change_status(task_repo, project_repo):
    p = project_repo.create(name="TP2", description="d")
    t = task_repo.create(project_id=p.id, title="T2", description="d")
    updated = task_repo.change_status(t.id, StatusEnum.DOING)
    assert updated is not None
    assert updated.status == StatusEnum.DOING