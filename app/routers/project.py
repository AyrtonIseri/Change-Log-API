from fastapi import status, HTTPException, Depends, Response, APIRouter
from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.types import Date
from . import oauth2
from typing import Optional
from .update import query_update
from datetime import datetime

def get_all_updates(project_id: int, db: Session, limit: int, skip: int) -> list[schemas.Update]:
    '''
    queries the database and returns all updates for a given project
    '''

    update_ids = db.query(models.Updates.id).filter(models.Updates.project_id == project_id).order_by(models.Updates.creation_date.desc()).offset(skip).limit(limit).all()
    update_ids = [id[0] for id in update_ids]
    update_list = []

    for update_id in update_ids:
        update_list.append(query_update(update_id, db))

    return update_list


router = APIRouter(
    prefix='/projects',
    tags=['Projects']
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.Project])
def get_projects(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user),
                limit: int = 10, skip = 0, search: Optional[str] = "", update_limit: int = 2, update_skip: int = 0, date: str = "", creator: int = None):

    projects_query = db.query(models.Projects).filter(models.Projects.title.contains(search))

    if date != "":
        try:
            date = datetime.strptime(date, "%Y-%m-%d").date()
            projects_query = projects_query.filter(models.Projects.creation_date.cast(Date) == date)
        except:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{date} not formatted correctly")

    if creator:
        projects_query = projects_query.filter(models.Projects.created_by == creator)

    projects = projects_query.order_by(models.Projects.creation_date.desc()).limit(limit).offset(skip).all()

    for project in projects:
        project.project_updates = get_all_updates(project_id=project.id, db=db, limit=update_limit, skip=update_skip)

    return projects


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Project)
def get_project(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user), 
                update_limit: int = 2, update_skip: int = 0):

    project_query = db.query(models.Projects).filter(models.Projects.id == id)
    project = project_query.first()

    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with id {id} not found.")

    project.project_updates = get_all_updates(project_id = id, db=db, limit=update_limit, skip=update_skip)

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

    project = project_query.first()
    project.project_updates = get_all_updates(project_id=id, db=db, limit=10, skip=0)

    return project_query.first()
