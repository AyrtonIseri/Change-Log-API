from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional

class BaseProject(BaseModel):
    project_name: str
    project_active: bool
    project_creator: str
    
    class Config:
        orm_mode = True

class ProjectCreate(BaseProject):
    pass

class Project(BaseProject):
    created_date: datetime
    

class BaseUser(BaseModel):
    username: str

    @validator('username')
    def name_must_be_formatted(cls, v):
        assert v.isalnum(), "username must be an alphanumeric"
        return v

    class Config:
        orm_mode=True

        
class UserCreate(BaseUser):
    password: str

class User(BaseUser):
    created_date: datetime

class UserAuth(BaseModel):
    username: str
    password: str
    
    @validator('username')
    def name_must_be_formatted(cls, v):
        assert v.isalnum(), "username must be an alphanumeric"
        return v

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int