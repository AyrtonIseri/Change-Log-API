from fastapi import status, HTTPException, Depends, Response, APIRouter
from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/projects',
    tags=['Projects']
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.Project])
def get_updates(db: Session = Depends(get_db)):
    projects = db.query(models.Projects).all()

    return projects

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Project)
def get_update(id: int, db: Session = Depends(get_db)):
    project_query = db.query(models.Projects).filter(models.Projects.project_id == id)
    project = project_query.first()

    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with id {id} not found.")
    
    return project

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):

    new_project = models.Projects(**project.dict())

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(id: int, db: Session = Depends(get_db)):
    delete_query = db.query(models.Projects).filter(models.Projects.project_id == id)
    project = delete_query.first()

    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with id {id} not found.")
    
    delete_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Project)
def update_project(id: int, updated_project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    
    project_query = db.query(models.Projects).filter(models.Projects.project_id == id)
    project = project_query.first()

    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with id {id} not found.")
    
    project_query.update(updated_project.dict(), synchronize_session=False)

    db.commit()

    return project_query.first()
