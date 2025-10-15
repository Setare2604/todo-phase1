import os
from dotenv import load_dotenv

load_dotenv() 

class Settings:
    def __init__(self):
        self.max_projects = int(os.getenv("MAX_NUMBER_OF_PROJECTS", 10))
        self.max_tasks_per_project = int(os.getenv("MAX_NUMBER_OF_TASKS_PER_PROJECT", 50))

_settings_instance = None

def get_settings():
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings()
    return _settings_instance