# 📝 ToDo List Manager (Phase 1 - In-Memory Storage)

This project is **Phase 1** of the ToDo List Management System, implemented in **Python** using **Object-Oriented Programming (OOP)** and **In-Memory Storage**.  
The goal of this phase is to build a modular, layered, and clean foundation of the system, ready for future phases that will include database persistence and web API integration.

---

## 🎯 Main Objectives and Features

- Modular and layered architecture (Config, Core, Storage, CLI)
- Follows **Clean Code** and **PEP8** conventions
- Implements all core project and task management features
- Uses **dotenv** for configuration via `.env` file
- Ready for **Persistence Layer** in later phases
- Dependency management via **Poetry**

---

## 🧩 Project Structure

```
todo_cli/
│
├── cli/                  # Command Line Interface (CLI)
│   └── main.py
│
├── core/                 # Business Logic Layer
│   ├── models.py
│   └── services.py
│
├── storage/              # In-Memory Data Storage
│   └── in_memory_storage.py
│
├── config/               # Configuration and environment variables
│   └── settings.py
│
├── tests/                # Unit Tests (optional)
│
├── .env                  # Environment variables
├── .env.example          # Example configuration file
├── pyproject.toml        # Poetry configuration file
├── poetry.lock
└── README.md
```

---

## ⚙️ How to Run the Project

### 1️⃣ Install Dependencies
Make sure Poetry is installed, then run:
```bash
poetry install
```

### 2️⃣ Run the Application
```bash
poetry run python todo_cli/cli/main.py
```

### 3️⃣ Environment Variables
Define environment variables in `.env`:
```
MAX_NUMBER_OF_PROJECTS=10
MAX_NUMBER_OF_TASKS_PER_PROJECT=50
```

---

## 🧠 Implemented Features (Phase 1)

| # | Feature | Description |
|---|----------|-------------|
| 1️⃣ | Create Project | Add a new project with name and description validation |
| 2️⃣ | Edit Project | Update project name and description |
| 3️⃣ | Delete Project | Delete a project and all its tasks (Cascade Delete) |
| 4️⃣ | Add Task | Add a new task with deadline validation |
| 5️⃣ | Edit Task | Modify title, description, and deadline |
| 6️⃣ | Change Task Status | Switch between todo / doing / done |
| 7️⃣ | Delete Task | Remove a specific task |
| 8️⃣ | List Projects | Show all projects with task summary |
| 9️⃣ | List Tasks in Project | Display all tasks within a selected project |

---

## 🧩 Architecture Overview

- **In-Memory Storage:** All data is stored temporarily in memory (no persistence yet).  
- **Core Layer:** Defines main business logic and data models (`Project`, `Task`, etc.).  
- **CLI Layer:** Handles user interaction through command-line interface.  
- **Config Layer:** Loads environment configurations using `.env`.

This layered structure ensures that persistence or API layers can be added later without modifying the core logic.

---

## 🧭 Git Branching Policy

| Branch | Description |
|--------|--------------|
| `main` | Stable production-ready branch |
| `develop` | Active development branch |
| `feature/*` | Used for implementing new features |

Example workflow:

```bash
# Start from develop branch
git checkout develop

# Create a new feature branch
git checkout -b feature/add-task

# Add and commit changes
git add .
git commit -m "feat: add task creation feature"

# Push feature branch to GitHub
git push origin feature/add-task

# Open Pull Request (feature → develop)
# After review, merge develop → main for stable release
```

---

## 📦 Dependency Management with Poetry

Poetry is used as a modern dependency and project manager for Python.  
Main advantages:
- Automatically creates a virtual environment per project  
- Tracks dependencies in `pyproject.toml`  
- Runs the project easily using `poetry run`  
- Simple and consistent installation with `poetry install`

---
