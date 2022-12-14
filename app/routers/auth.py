from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import UserAuth, User, Token
from .. import models
from ..utils import verify
from .oauth2 import create_access_token


router = APIRouter(
    prefix="/login", 
    tags=['auth']
    )

@router.post('/', response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.username == user_credentials.username).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    password_credentials = user_credentials.password

    if not verify(password_credentials, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    token = create_access_token(payload_data={"user_id": user.id})

    return {"access_token": token, "token_type": "bearer"}