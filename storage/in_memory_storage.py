class InMemoryStorage:

    def __init__(self):
        self._projects = {}  # {project_id: Project object}
        self._tasks = {}     # {task_id: Task object}
        self._project_id_counter = 1
        self._task_id_counter = 1

    def create_project(self, project):
        project.project_id = self._project_id_counter
        self._projects[self._project_id_counter] = project
        self._project_id_counter += 1
        return project

    def get_all_projects(self):
        return list(self._projects.values())

    def get_project_by_id(self, project_id):
        return self._projects.get(project_id)

    def update_project(self, project):
        if project.project_id in self._projects:
            self._projects[project.project_id] = project
            return True
        return False

    def delete_project(self, project_id):
        if project_id in self._projects:
            del self._projects[project_id]
            # Cascade Delete: حذف تمام تسک‌های مرتبط با این پروژه
            task_ids_to_delete = [task_id for task_id, task in self._tasks.items() if task.project_id == project_id]
            for task_id in task_ids_to_delete:
                del self._tasks[task_id]
            return True
        return False

    def create_task(self, task):
        task.task_id = self._task_id_counter
        self._tasks[self._task_id_counter] = task
        self._task_id_counter += 1
        return task

    def get_tasks_by_project_id(self, project_id):
        return [task for task in self._tasks.values() if task.project_id == project_id]

    def get_task_by_id(self, task_id):
        return self._tasks.get(task_id)

    def update_task(self, task):
        if task.task_id in self._tasks:
            self._tasks[task.task_id] = task
            return True
        return False

    def delete_task(self, task_id):
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False