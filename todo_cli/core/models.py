from datetime import datetime
from enum import Enum

class TaskStatus(Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"

class Project:
    def __init__(self, project_id: int, name: str, description: str):
        self.project_id = project_id
        self.name = name
        self.description = description
        self.created_at = datetime.now()

    def __str__(self):
        return f"Project(ID: {self.project_id}, Name: {self.name})"

class Task:
    def __init__(self, task_id: int, project_id: int, title: str, description: str, status: TaskStatus = TaskStatus.TODO, deadline: datetime = None):
        self.task_id = task_id
        self.project_id = project_id
        self.title = title
        self.description = description
        self.status = status
        self.deadline = deadline
        self.created_at = datetime.now()

    def __str__(self):
        return f"Task(ID: {self.task_id}, Title: {self.title}, Status: {self.status.value})"