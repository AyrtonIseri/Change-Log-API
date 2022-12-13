from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    user.password = utils.hash(user.password)

    user_query = db.query(models.Users).filter(models.Users.username == user.username)
    if user_query.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Username already registered.")

    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.User)
def get_user(id: int, db: Session = Depends(get_db)):
    query_user = db.query(models.Users).filter(models.Users.id == id).first()

    if query_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Couldn't find user of id {id}.")
    
    return query_user