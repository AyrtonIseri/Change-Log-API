from fastapi import status, HTTPException, Depends, Response, APIRouter
from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session
from . import oauth2
from typing import Optional

router = APIRouter(
    prefix='/projects',
    tags=['Projects']
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.Project])
def get_projects(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user),
                limit: int = 10, skip = 0, search: Optional[str] = ""):
    
    projects = db.query(models.Projects).filter(models.Projects.title.contains(search)).limit(limit).offset(skip).all()

    return projects

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Project)
def get_project(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user),
                limit: int = 10, skip = 0, search: Optional[str] = ""):

    project_query = db.query(models.Projects).filter(models.Projects.id == id).limit(limit).offset(skip)
    project = project_query.first()

    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with id {id} not found.")

    return project

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db),
                   current_user = Depends(oauth2.get_current_user)):

    new_project = models.Projects(created_by = current_user.id, **project.dict())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):

    delete_query = db.query(models.Projects).filter(models.Projects.id == id)
    project = delete_query.first()

    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with id {id} not found.")

    delete_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Project)
def update_project(id: int, updated_project: schemas.ProjectCreate, db: Session = Depends(get_db),
                   current_user = Depends(oauth2.get_current_user)):

    project_query = db.query(models.Projects).filter(models.Projects.id == id)
    project = project_query.first()

    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with id {id} not found.")
    
    project_query.update(updated_project.dict(), synchronize_session=False)

    db.commit()

    return project_query.first()
