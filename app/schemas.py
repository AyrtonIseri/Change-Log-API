from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional

#-----------------------------------------------------------------------------

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
    creation_date: datetime

#-----------------------------------------------------------------------------

class UserAuth(BaseModel):
    username: str
    password: str
    
    @validator('username')
    def name_must_be_formatted(cls, v):
        assert v.isalnum(), "username must be an alphanumeric"
        return v

#-----------------------------------------------------------------------------

class BasePoints(BaseModel):
    title: str
    description: Optional[list[str]]

    class Config:
        orm_mode=True

class PointsCreate(BasePoints):
    pass

class Points(BasePoints):
    pass


#-----------------------------------------------------------------------------

class BaseUpdate(BaseModel):
    title: str
    relevant_points: Optional[list[PointsCreate]]

    class Config:
        orm_mode=True

class UpdateCreate(BaseUpdate):
    project_id: int

class Update(BaseUpdate):
    id: int
    created_by: str
    creation_date: datetime


#-----------------------------------------------------------------------------

class BaseProject(BaseModel):
    title: str
    active: Optional[bool]

    class Config:
        orm_mode = True

class ProjectCreate(BaseProject):
    pass

class Project(BaseProject):
    id: int
    creation_date: datetime
    created_by: str
    project_updates: Optional[list[Update]]

#-----------------------------------------------------------------------------

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int

#-----------------------------------------------------------------------------

