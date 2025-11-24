from app.models.project import Project
from todo_cli.core.models import Project as DomainProject

def test_project_create_and_get(project_repo):
    # create project
    p = project_repo.create(name="Test Project", description="desc")
    assert p.id is not None
    assert p.name == "Test Project"

    # get by id
    fetched = project_repo.get(p.id)
    assert fetched is not None
    assert fetched.name == "Test Project"

def test_get_by_name(project_repo):
    p = project_repo.create(name="UniqueName", description="x")
    found = project_repo.get_by_name("UniqueName")
    assert found is not None
    assert found.id == p.id

def test_list_and_delete(project_repo):
    project_repo.create(name="P1", description="")
    project_repo.create(name="P2", description="")
    all_projects = project_repo.list()
    assert len(all_projects) >= 2

    # delete
    pid = all_projects[0].id
    project_repo.delete(pid)
    assert project_repo.get(pid) is None
