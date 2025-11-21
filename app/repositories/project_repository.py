from typing import List
from sqlalchemy.orm import Session
from app.models.project import Project

class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str, description: str) -> Project:
        p = Project(name=name, description=description)
        self.db.add(p)
        self.db.commit()
        self.db.refresh(p)
        return p

    def get(self, project_id: int) -> Project | None:
        return self.db.query(Project).filter(Project.id == project_id).first()

    def list(self) -> List[Project]:
        return self.db.query(Project).all()

    def delete(self, project_id: int):
        p = self.get(project_id)
        if p:
            self.db.delete(p)
            self.db.commit()