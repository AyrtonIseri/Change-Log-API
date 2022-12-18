from fastapi import status, HTTPException, Depends, Response, APIRouter
from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session
from . import oauth2

def post_relevant_points(relevant_points: list[schemas.PointsCreate], update_id: int, 
                        db: Session):
    for relevant_point in relevant_points:
        title, desc = relevant_point.values()
        new_relevant_point = models.Points(update_id=update_id, title=title,
                                           description=desc)
        db.add(new_relevant_point)
        db.commit()

def query_update(update_id: int, db: Session):
    update = db.query(models.Updates).filter(models.Updates.id == update_id).first()
    relevant_points = db.query(models.Points).filter(models.Points.update_id == update_id).all()
    update.relevant_points = relevant_points
    return update



router = APIRouter(
    prefix='/updates',
    tags=['updates']
)

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Update)
def create_update(update: schemas.UpdateCreate, db: Session = Depends(get_db),
                   current_user = Depends(oauth2.get_current_user)):

    title, relevant_points, project_id = update.dict().values()

    project = db.query(models.Projects).filter(models.Projects.id == project_id).first()

    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with id {project_id} not found.")

    new_update = models.Updates(project_id=project_id, title=title, 
                                created_by=current_user.id)

    db.add(new_update)
    db.commit()
    db.refresh(new_update)

    update_id = new_update.id
    post_relevant_points(relevant_points, update_id, db)
    new_update = query_update(update_id=update_id, db=db)

    return new_update


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):

    delete_query = db.query(models.Updates).filter(models.Updates.id == id)
    project = delete_query.first()

    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Update with id {id} not found.")

    delete_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# --------------------------------------- im here --------------------------

@router.put("/{id}", response_model=schemas.Update)
def update_project(id: int, updated_update: schemas.UpdateCreate, db: Session = Depends(get_db),
                   current_user = Depends(oauth2.get_current_user)):

    update_query = db.query(models.Updates).filter(models.Updates.id == id)
    update = update_query.first()

    if update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Update with id {id} not found.")

    relevant_points = db.query(models.Points).filter(models.Points.update_id == id)
    relevant_points.delete(synchronize_session=False)
    db.commit()

    title, relevant_points, project_id = updated_update.dict().values()
    post_relevant_points(relevant_points, id, db)
    update_query.update({'title':title, 'project_id':project_id},  synchronize_session=False)
    db.commit()

    new_update = query_update(update_id=id, db=db)

    return new_update
