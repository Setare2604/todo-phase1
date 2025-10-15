from datetime import datetime
from todo_cli.core.models import Project, Task, TaskStatus
from todo_cli.storage.in_memory_storage import InMemoryStorage
from todo_cli.config.settings import get_settings

settings = get_settings()


class ProjectService:

    def __init__(self, storage: InMemoryStorage):
        self.storage = storage

    def create_project(self, name: str, description: str) -> Project:
        """
        Creating a new project with the necessary validations
        
        Args:
            name: Project name
            description: Project Description
            
        Returns:
            Project: Project object created
            
        Raises:
            ValueError: In case of violation of any of the rules
        """
        if len(self.storage.get_all_projects()) >= settings.max_projects:
            raise ValueError(f"The maximum number of projects allowed ({settings.max_projects}) has been reached.")

        existing_projects = self.storage.get_all_projects()
        if any(p.name == name for p in existing_projects):
            raise ValueError("The project name is duplicated.")

        if not (0 < len(name) <= 30):
            raise ValueError("The project name must be between 1 and 30 characters.")
        if not (0 < len(description) <= 150):
            raise ValueError("Project descriptions must be between 1 and 150 characters.")

        new_project = Project(0, name, description) 
        return self.storage.create_project(new_project)

    def edit_project(self, project_id: int, new_name: str, new_description: str) -> bool:
        """
        Edit project information
        
        Args:
            project_id: Project ID
            new_name: New project name
            new_description: New project description
            
        Returns:
            bool: True on success, False on failure
        """
        project = self.storage.get_project_by_id(project_id)
        if not project:
            raise ValueError("The desired project was not found.")

        existing_projects = self.storage.get_all_projects()
        if any(p.name == new_name and p.project_id != project_id for p in existing_projects):
            raise ValueError("The new project name conflicts with another project.")

        if not (0 < len(new_name) <= 30):
            raise ValueError("The project name must be between 1 and 30 characters.")
        if not (0 < len(new_description) <= 150):
            raise ValueError("Project descriptions must be between 1 and 150 characters.")

        project.name = new_name
        project.description = new_description
        return self.storage.update_project(project)

    def delete_project(self, project_id: int) -> bool:
        """
        (Cascade Delete)
        
        Args:
            project_id: Project ID
            
        Returns:
            bool: True on success, False on failure
        """
        project = self.storage.get_project_by_id(project_id)
        if not project:
            raise ValueError("The desired project was not found.")

    # Delete the project (which will automatically delete its tasks)
        return self.storage.delete_project(project_id)

    def get_all_projects(self) -> list[Project]:
        """
        Get a list of all projects
        
        Returns:
            list[Project]: List of all projects
        """
        return self.storage.get_all_projects()

    def get_project_by_id(self, project_id: int) -> Project:
        """
        Get project by ID
        
        Args:
            project_id: Project ID
            
        Returns:
            Project: Project object
        """
        project = self.storage.get_project_by_id(project_id)
        if not project:
            raise ValueError("The desired project was not found.")
        return project


class TaskService:

    def __init__(self, storage: InMemoryStorage):
        self.storage = storage

    def create_task(self, project_id: int, title: str, description: str, deadline: datetime = None) -> Task:
        """
        Creating a new task in a project
        
        Args:
            project_id: Parent project ID
            title: Task title
            description: Task description
            deadline: Deadline date (optional)
            
        Returns:
            Task: Task object created
        """
        project = self.storage.get_project_by_id(project_id)
        if not project:
            raise ValueError("The desired project was not found.")

        project_tasks = self.storage.get_tasks_by_project_id(project_id)
        if len(project_tasks) >= settings.max_tasks_per_project:
            raise ValueError(f"Maximum number of tasks allowed in a project({settings.max_tasks_per_project}) has been reached.")

        if not (0 < len(title) <= 30):
            raise ValueError("The task title must be between 1 and 30 characters.")
        if not (0 < len(description) <= 150):
            raise ValueError("Task descriptions must be between 1 and 150 characters.")

        if deadline and deadline < datetime.now():
            raise ValueError("The deadline date cannot be in the past.")

        new_task = Task(0, project_id, title, description, TaskStatus.TODO, deadline)
        return self.storage.create_task(new_task)

    def change_task_status(self, task_id: int, new_status: TaskStatus) -> bool:
        """
        Changing the status of a task
        
        Args:
            task_id: Task ID
            new_status: New status
            
        Returns:
            bool: True If successful
        """
        task = self.storage.get_task_by_id(task_id)
        if not task:
            raise ValueError("The requested task was not found.")

        # Checking the validity of the new status
        if not isinstance(new_status, TaskStatus):
            raise ValueError("The status provided is not valid.")

        task.status = new_status
        return self.storage.update_task(task)

    def edit_task(self, task_id: int, new_title: str = None, new_description: str = None, 
                 new_status: TaskStatus = None, new_deadline: datetime = None) -> bool:
        """
        Edit task information
        
        Args:
            task_id: task_id
            new_title: New title (optional)
            new_description: New description (optional)
            new_status: New status (optional)
            new_deadline: New deadline (optional)
            
        Returns:
            bool: True If successful
        """
        task = self.storage.get_task_by_id(task_id)
        if not task:
            raise ValueError("The requested task was not found.")

        # Field validation
        if new_title is not None:
            if not (0 < len(new_title) <= 30):
                raise ValueError("The task title must be between 1 and 30 characters.")
            task.title = new_title

        if new_description is not None:
            if not (0 < len(new_description) <= 150):
                raise ValueError("Task descriptions must be between 1 and 150 characters.")
            task.description = new_description

        if new_status is not None:
            if not isinstance(new_status, TaskStatus):
                raise ValueError("The status provided is not valid.")
            task.status = new_status

        if new_deadline is not None:
            if new_deadline < datetime.now():
                raise ValueError("The deadline date cannot be in the past.")
            task.deadline = new_deadline

        return self.storage.update_task(task)

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task
        
        Args:
            task_id: Task ID
            
        Returns:
            bool: True If successful
        """
        # Checking for the existence of a task
        task = self.storage.get_task_by_id(task_id)
        if not task:
            raise ValueError("The requested task was not found.")

        return self.storage.delete_task(task_id)

    def get_task_by_id(self, task_id: int) -> Task:
        """
        Get task by ID
        
        Args:
            task_id: Task ID
            
        Returns:
            Task: Task object
        """
        task = self.storage.get_task_by_id(task_id)
        if not task:
            raise ValueError("The requested task was not found.")
        return task

    def get_tasks_by_project_id(self, project_id: int) -> list[Task]:
        """
        Get all tasks in a project
        
        Args:
            project_id: Project ID
            
        Returns:
            list[Task]: Project task list
        """
        # Checking the existence of the project
        project = self.storage.get_project_by_id(project_id)
        if not project:
            raise ValueError("The desired project was not found.")

        return self.storage.get_tasks_by_project_id(project_id)

    def get_all_tasks(self) -> list[Task]:
        """
        Receive all system tasks (for management purposes)
        
        Returns:
            list[Task]: List of all tasks
        """
        
        return list(self.storage._tasks.values())