from datetime import datetime, timedelta
from jose import JWTError, jwt
from .. import schemas, database, models
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..config import env_settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = env_settings.secret_key
ALGORITHM = env_settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = env_settings.access_token_expire_minutes

def create_access_token(payload_data: dict):
    payload_to_encode = payload_data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload_to_encode["exp"] = expire

    jwt_token = jwt.encode(payload_to_encode, key=SECRET_KEY, algorithm=ALGORITHM)

    return jwt_token

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY)

        id = payload['user_id']

        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    token_data = verify_access_token(token, credentials_exception)

    user = db.query(models.Users).filter(models.Users.id == token_data.id).first()

    return user