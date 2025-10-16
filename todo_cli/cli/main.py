"""
ToDo List Manager - CLI Interface
Main entry point for the ToDo List application
"""

from todo_cli.core.services import ProjectService, TaskService
from todo_cli.storage.in_memory_storage import InMemoryStorage
from todo_cli.core.models import TaskStatus
from datetime import datetime
import re


class ToDoListCLI:
    """Command Line Interface for ToDo List Management"""
    
    def __init__(self):
        self.storage = InMemoryStorage()
        self.project_service = ProjectService(self.storage)
        self.task_service = TaskService(self.storage)
        self.current_project_id = None
    
    def display_main_menu(self):
        """Display the main menu"""
        print("\n" + "="*50)
        print("        TO-DO LIST MANAGER")
        print("="*50)
        print("1. Project Management")
        print("2. Task Management")
        print("3. Switch to Project")
        print("4. Display Current Project Tasks")
        print("0. Exit")
        print("-"*50)
    
    def display_project_menu(self):
        """Display project management menu"""
        print("\n" + "-"*40)
        print("      PROJECT MANAGEMENT")
        print("-"*40)
        print("1. Create New Project")
        print("2. List All Projects")
        print("3. Edit Project")
        print("4. Delete Project")
        print("5. Back to Main Menu")
        print("-"*40)
    
    def display_task_menu(self):
        """Display task management menu"""
        if not self.current_project_id:
            print("❌ Please select a project first!")
            return False
        
        project = self.storage.get_project_by_id(self.current_project_id)
        if not project:
            print("❌ Selected project not found!")
            self.current_project_id = None
            return False
        
        print(f"\n" + "-"*40)
        print(f"   TASK MANAGEMENT - {project.name.upper()}")
        print("-"*40)
        print("1. Add New Task")
        print("2. List All Tasks in Project")
        print("3. Edit Task")
        print("4. Change Task Status")
        print("5. Delete Task")
        print("6. Back to Main Menu")
        print("-"*40)
        return True
    
    def get_user_input(self, prompt, validator=None):
        """Get user input with optional validation"""
        while True:
            try:
                user_input = input(prompt).strip()
                if validator:
                    return validator(user_input)
                return user_input
            except ValueError as e:
                print(f"❌ Invalid input: {e}")
            except KeyboardInterrupt:
                print("\n\nOperation cancelled by user.")
                return None
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
    
    def validate_not_empty(self, text, field_name):
        """Validate that input is not empty"""
        if not text:
            raise ValueError(f"{field_name} cannot be empty!")
        return text
    
    def validate_length(self, text, field_name, max_length):
        """Validate input length"""
        text = self.validate_not_empty(text, field_name)
        if len(text) > max_length:
            raise ValueError(f"{field_name} must be {max_length} characters or less!")
        return text
    
    def validate_date(self, date_string):
        """Validate and parse date input"""
        if not date_string:
            return None
        
        try:
            # Try different date formats
            for fmt in ['%Y-%m-%d', '%Y/%m/%d', '%d-%m-%Y', '%d/%m/%Y']:
                try:
                    return datetime.strptime(date_string, fmt).date()
                except ValueError:
                    continue
            raise ValueError("Invalid date format. Use YYYY-MM-DD, DD-MM-YYYY, etc.")
        except Exception:
            raise ValueError("Invalid date format. Use YYYY-MM-DD, DD-MM-YYYY, etc.")
    
    def select_project(self):
        """Select a project to work with"""
        projects = self.project_service.get_all_projects()
        if not projects:
            print("❌ No projects available. Please create a project first.")
            return None
        
        print("\nAvailable Projects:")
        print("-" * 30)
        for project in projects:
            tasks = self.task_service.get_tasks_by_project_id(project.project_id)
            task_count = len(tasks)
            print(f"{project.project_id}. {project.name} ({task_count} tasks)")
            print(f"   Description: {project.description}")
            print()
        
        def validate_project_choice(choice):
            try:
                project_id = int(choice)
                project = self.storage.get_project_by_id(project_id)
                if not project:
                    raise ValueError("Project ID not found!")
                return project_id
            except ValueError:
                raise ValueError("Please enter a valid project number!")
        
        project_id = self.get_user_input(
            "Enter project number to select: ",
            validate_project_choice
        )
        
        if project_id:
            project = self.storage.get_project_by_id(project_id)
            print(f"✅ Switched to project: {project.name}")
            return project_id
        
        return None
    
    def handle_project_creation(self):
        """Handle creating a new project"""
        print("\n--- Create New Project ---")
        
        name = self.get_user_input(
            "Project name (max 30 chars): ",
            lambda x: self.validate_length(x, "Project name", 30)
        )
        if not name:
            return
        
        description = self.get_user_input(
            "Project description (max 150 chars): ",
            lambda x: self.validate_length(x, "Project description", 150)
        )
        if not description:
            return
        
        try:
            new_project = self.project_service.create_project(name, description)
            print(f"✅ Project '{new_project.name}' created successfully!")
            
            # Ask if user wants to switch to this project
            switch = self.get_user_input("Switch to this project? (y/n): ").lower()
            if switch in ['y', 'yes']:
                self.current_project_id = new_project.project_id
                print(f"✅ Switched to project: {new_project.name}")
                
        except ValueError as e:
            print(f"❌ Error creating project: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
    
    def handle_project_listing(self):
        """Handle listing all projects"""
        projects = self.project_service.get_all_projects()
        
        if not projects:
            print("📭 No projects found.")
            return
        
        print(f"\n--- All Projects ({len(projects)}) ---")
        print("=" * 60)
        
        for project in projects:
            tasks = self.task_service.get_tasks_by_project_id(project.project_id)
            todo_count = len([t for t in tasks if t.status == TaskStatus.TODO])
            doing_count = len([t for t in tasks if t.status == TaskStatus.DOING])
            done_count = len([t for t in tasks if t.status == TaskStatus.DONE])
            
            print(f"ID: {project.project_id}")
            print(f"Name: {project.name}")
            print(f"Description: {project.description}")
            print(f"Tasks: 📋 Total: {len(tasks)} | ✅ Done: {done_count} | 🔄 Doing: {doing_count} | ⏳ Todo: {todo_count}")
            print(f"Created: {project.created_at.strftime('%Y-%m-%d %H:%M')}")
            print("-" * 60)
    
    def handle_project_edit(self):
        """Handle editing a project"""
        projects = self.project_service.get_all_projects()
        if not projects:
            print("❌ No projects available to edit.")
            return
        
        self.handle_project_listing()
        
        def validate_project_id(choice):
            try:
                project_id = int(choice)
                if not self.storage.get_project_by_id(project_id):
                    raise ValueError("Project ID not found!")
                return project_id
            except ValueError:
                raise ValueError("Please enter a valid project number!")
        
        project_id = self.get_user_input(
            "Enter project ID to edit: ",
            validate_project_id
        )
        if not project_id:
            return
        
        project = self.storage.get_project_by_id(project_id)
        print(f"\nEditing Project: {project.name}")
        print(f"Current description: {project.description}")
        
        new_name = self.get_user_input(
            f"New name (current: '{project.name}', press Enter to keep): ",
            lambda x: self.validate_length(x or project.name, "Project name", 30)
        )
        if not new_name:
            return
        
        new_description = self.get_user_input(
            f"New description (current: '{project.description}', press Enter to keep): ",
            lambda x: self.validate_length(x or project.description, "Project description", 150)
        )
        if not new_description:
            return
        
        # Use original values if user pressed Enter
        new_name = new_name if new_name != project.name else project.name
        new_description = new_description if new_description != project.description else project.description
        
        try:
            success = self.project_service.edit_project(project_id, new_name, new_description)
            if success:
                print("✅ Project updated successfully!")
            else:
                print("❌ Failed to update project!")
        except ValueError as e:
            print(f"❌ Error updating project: {e}")
    
    def handle_project_deletion(self):
        """Handle deleting a project"""
        projects = self.project_service.get_all_projects()
        if not projects:
            print("❌ No projects available to delete.")
            return
        
        self.handle_project_listing()
        
        def validate_project_id(choice):
            try:
                project_id = int(choice)
                if not self.storage.get_project_by_id(project_id):
                    raise ValueError("Project ID not found!")
                return project_id
            except ValueError:
                raise ValueError("Please enter a valid project number!")
        
        project_id = self.get_user_input(
            "Enter project ID to delete: ",
            validate_project_id
        )
        if not project_id:
            return
        
        project = self.storage.get_project_by_id(project_id)
        
        # Confirm deletion
        confirm = self.get_user_input(
            f"⚠️  Are you sure you want to delete project '{project.name}' and ALL its tasks? This cannot be undone! (yes/no): "
        )
        
        if confirm.lower() in ['yes', 'y']:
            try:
                success = self.project_service.delete_project(project_id)
                if success:
                    print("✅ Project and all its tasks deleted successfully!")
                    # Clear current project if it was deleted
                    if self.current_project_id == project_id:
                        self.current_project_id = None
                        print("ℹ️  Current project cleared.")
                else:
                    print("❌ Failed to delete project!")
            except ValueError as e:
                print(f"❌ Error deleting project: {e}")
        else:
            print("❌ Deletion cancelled.")
    
    def handle_task_creation(self):
        """Handle creating a new task"""
        if not self.current_project_id:
            print("❌ Please select a project first!")
            return
        
        print("\n--- Create New Task ---")
        
        title = self.get_user_input(
            "Task title (max 30 chars): ",
            lambda x: self.validate_length(x, "Task title", 30)
        )
        if not title:
            return
        
        description = self.get_user_input(
            "Task description (max 150 chars): ",
            lambda x: self.validate_length(x, "Task description", 150)
        )
        if not description:
            return
        
        deadline = self.get_user_input(
            "Deadline (optional - format: YYYY-MM-DD): ",
            self.validate_date
        )
        if deadline is None and deadline != "":
            return
        
        try:
            new_task = self.task_service.create_task(
                self.current_project_id, title, description, deadline
            )
            print(f"✅ Task '{new_task.title}' created successfully!")
            print(f"   Status: {new_task.status.value.upper()}")
            if new_task.deadline:
                print(f"   Deadline: {new_task.deadline}")
                
        except ValueError as e:
            print(f"❌ Error creating task: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
    
    def handle_task_listing(self):
        """Handle listing all tasks in current project"""
        if not self.current_project_id:
            print("❌ Please select a project first!")
            return
        
        project = self.storage.get_project_by_id(self.current_project_id)
        tasks = self.task_service.get_tasks_by_project_id(self.current_project_id)
        
        if not tasks:
            print(f"📭 No tasks found in project '{project.name}'.")
            return
        
        # Group tasks by status
        todo_tasks = [t for t in tasks if t.status == TaskStatus.TODO]
        doing_tasks = [t for t in tasks if t.status == TaskStatus.DOING]
        done_tasks = [t for t in tasks if t.status == TaskStatus.DONE]
        
        print(f"\n--- Tasks in '{project.name}' ({len(tasks)} total) ---")
        print("=" * 70)
        
        def print_task_group(group, status, icon):
            if group:
                print(f"\n{icon} {status.upper()} ({len(group)}):")
                print("-" * 40)
                for task in group:
                    deadline_str = f" | 📅 {task.deadline}" if task.deadline else ""
                    print(f"  #{task.task_id}: {task.title}{deadline_str}")
                    print(f"     Description: {task.description}")
                    print(f"     Created: {task.created_at.strftime('%Y-%m-%d %H:%M')}")
        
        print_task_group(todo_tasks, "todo", "⏳")
        print_task_group(doing_tasks, "doing", "🔄")
        print_task_group(done_tasks, "done", "✅")
        
        # Summary
        print(f"\n📊 Summary: ⏳ {len(todo_tasks)} | 🔄 {len(doing_tasks)} | ✅ {len(done_tasks)}")
    
    def handle_task_edit(self):
        """Handle editing a task"""
        if not self.current_project_id:
            print("❌ Please select a project first!")
            return
        
        tasks = self.task_service.get_tasks_by_project_id(self.current_project_id)
        if not tasks:
            print("❌ No tasks available to edit.")
            return
        
        # Show available tasks
        project = self.storage.get_project_by_id(self.current_project_id)
        print(f"\nTasks in '{project.name}':")
        for task in tasks:
            status_icon = "⏳" if task.status == TaskStatus.TODO else "🔄" if task.status == TaskStatus.DOING else "✅"
            deadline_str = f" | 📅 {task.deadline}" if task.deadline else ""
            print(f"  #{task.task_id}: {status_icon} {task.title}{deadline_str}")
        
        def validate_task_id(choice):
            try:
                task_id = int(choice)
                task = self.storage.get_task_by_id(task_id)
                if not task or task.project_id != self.current_project_id:
                    raise ValueError("Task ID not found in current project!")
                return task_id
            except ValueError:
                raise ValueError("Please enter a valid task number!")
        
        task_id = self.get_user_input(
            "Enter task ID to edit: ",
            validate_task_id
        )
        if not task_id:
            return
        
        task = self.storage.get_task_by_id(task_id)
        print(f"\nEditing Task: {task.title}")
        print(f"Current description: {task.description}")
        print(f"Current status: {task.status.value}")
        print(f"Current deadline: {task.deadline or 'Not set'}")
        
        new_title = self.get_user_input(
            f"New title (current: '{task.title}', press Enter to keep): ",
            lambda x: self.validate_length(x or task.title, "Task title", 30)
        )
        if not new_title:
            return
        
        new_description = self.get_user_input(
            f"New description (current: '{task.description}', press Enter to keep): ",
            lambda x: self.validate_length(x or task.description, "Task description", 150)
        )
        if not new_description:
            return
        
        new_deadline = self.get_user_input(
            f"New deadline (current: '{task.deadline or 'Not set'}', press Enter to keep): ",
            lambda x: self.validate_date(x) if x else None
        )
        if new_deadline is None:
            new_deadline = task.deadline
        
        # Use original values if user pressed Enter
        new_title = new_title if new_title != task.title else task.title
        new_description = new_description if new_description != task.description else task.description
        new_deadline = new_deadline if new_deadline != "" else task.deadline
        
        try:
            success = self.task_service.edit_task(
                task_id, 
                new_title=new_title, 
                new_description=new_description, 
                new_deadline=new_deadline
            )
            if success:
                print("✅ Task updated successfully!")
            else:
                print("❌ Failed to update task!")
        except ValueError as e:
            print(f"❌ Error updating task: {e}")
    
    def handle_task_status_change(self):
        """Handle changing task status"""
        if not self.current_project_id:
            print("❌ Please select a project first!")
            return
        
        tasks = self.task_service.get_tasks_by_project_id(self.current_project_id)
        if not tasks:
            print("❌ No tasks available.")
            return
        
        # Show available tasks with current status
        print(f"\nCurrent Tasks:")
        for task in tasks:
            status_icon = "⏳" if task.status == TaskStatus.TODO else "🔄" if task.status == TaskStatus.DOING else "✅"
            print(f"  #{task.task_id}: {status_icon} {task.title} ({task.status.value})")
        
        def validate_task_id(choice):
            try:
                task_id = int(choice)
                task = self.storage.get_task_by_id(task_id)
                if not task or task.project_id != self.current_project_id:
                    raise ValueError("Task ID not found in current project!")
                return task_id
            except ValueError:
                raise ValueError("Please enter a valid task number!")
        
        task_id = self.get_user_input(
            "Enter task ID to change status: ",
            validate_task_id
        )
        if not task_id:
            return
        
        print("\nAvailable statuses:")
        print("1. ⏳ TODO")
        print("2. 🔄 DOING") 
        print("3. ✅ DONE")
        
        def validate_status_choice(choice):
            status_map = {'1': TaskStatus.TODO, '2': TaskStatus.DOING, '3': TaskStatus.DONE}
            if choice not in status_map:
                raise ValueError("Please enter 1, 2, or 3!")
            return status_map[choice]
        
        new_status = self.get_user_input(
            "Select new status (1-3): ",
            validate_status_choice
        )
        if not new_status:
            return
        
        try:
            success = self.task_service.change_task_status(task_id, new_status)
            if success:
                task = self.storage.get_task_by_id(task_id)
                status_icon = "⏳" if task.status == TaskStatus.TODO else "🔄" if task.status == TaskStatus.DOING else "✅"
                print(f"✅ Task status changed to: {status_icon} {task.status.value.upper()}")
            else:
                print("❌ Failed to change task status!")
        except ValueError as e:
            print(f"❌ Error changing task status: {e}")
    
    def handle_task_deletion(self):
        """Handle deleting a task"""
        if not self.current_project_id:
            print("❌ Please select a project first!")
            return
        
        tasks = self.task_service.get_tasks_by_project_id(self.current_project_id)
        if not tasks:
            print("❌ No tasks available to delete.")
            return
        
        # Show available tasks
        print(f"\nCurrent Tasks:")
        for task in tasks:
            status_icon = "⏳" if task.status == TaskStatus.TODO else "🔄" if task.status == TaskStatus.DOING else "✅"
            print(f"  #{task.task_id}: {status_icon} {task.title}")
        
        def validate_task_id(choice):
            try:
                task_id = int(choice)
                task = self.storage.get_task_by_id(task_id)
                if not task or task.project_id != self.current_project_id:
                    raise ValueError("Task ID not found in current project!")
                return task_id
            except ValueError:
                raise ValueError("Please enter a valid task number!")
        
        task_id = self.get_user_input(
            "Enter task ID to delete: ",
            validate_task_id
        )
        if not task_id:
            return
        
        task = self.storage.get_task_by_id(task_id)
        
        # Confirm deletion
        confirm = self.get_user_input(
            f"⚠️  Are you sure you want to delete task '{task.title}'? (yes/no): "
        )
        
        if confirm.lower() in ['yes', 'y']:
            try:
                success = self.task_service.delete_task(task_id)
                if success:
                    print("✅ Task deleted successfully!")
                else:
                    print("❌ Failed to delete task!")
            except ValueError as e:
                print(f"❌ Error deleting task: {e}")
        else:
            print("❌ Deletion cancelled.")
    
    def run(self):
        """Main application loop"""
        print("🚀 Welcome to ToDo List Manager!")
        print("📝 Manage your projects and tasks efficiently")
        
        while True:
            self.display_main_menu()
            
            choice = self.get_user_input("Enter your choice (0-4): ")
            if choice is None:
                continue
            
            if choice == "1":  # Project Management
                self.handle_project_operations()
            elif choice == "2":  # Task Management
                self.handle_task_operations()
            elif choice == "3":  # Switch Project
                self.current_project_id = self.select_project()
            elif choice == "4":  # Display Current Project Tasks
                if self.current_project_id:
                    self.handle_task_listing()
                else:
                    print("❌ Please select a project first!")
            elif choice == "0":  # Exit
                print("\n👋 Thank you for using ToDo List Manager! Goodbye!")
                break
            else:
                print("❌ Invalid choice! Please enter a number between 0-4.")
    
    def handle_project_operations(self):
        """Handle all project-related operations"""
        while True:
            self.display_project_menu()
            
            choice = self.get_user_input("Enter your choice (1-5): ")
            if choice is None:
                continue
            
            if choice == "1":
                self.handle_project_creation()
            elif choice == "2":
                self.handle_project_listing()
            elif choice == "3":
                self.handle_project_edit()
            elif choice == "4":
                self.handle_project_deletion()
            elif choice == "5":
                break
            else:
                print("❌ Invalid choice! Please enter a number between 1-5.")
    
    def handle_task_operations(self):
        """Handle all task-related operations"""
        while True:
            if not self.display_task_menu():
                break
            
            choice = self.get_user_input("Enter your choice (1-6): ")
            if choice is None:
                continue
            
            if choice == "1":
                self.handle_task_creation()
            elif choice == "2":
                self.handle_task_listing()
            elif choice == "3":
                self.handle_task_edit()
            elif choice == "4":
                self.handle_task_status_change()
            elif choice == "5":
                self.handle_task_deletion()
            elif choice == "6":
                break
            else:
                print("❌ Invalid choice! Please enter a number between 1-6.")


def main():
    """Main entry point for the application"""
    try:
        app = ToDoListCLI()
        app.run()
    except KeyboardInterrupt:
        print("\n\n👋 Program interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n💥 An unexpected error occurred: {e}")
        print("Please restart the application.")


if __name__ == "__main__":
    main()