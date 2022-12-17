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
    points_title: str
    descriptions: Optional[list[str]]

class PointsCreate(BasePoints):
    pass

class Points(BasePoints):
    points_id: int
    

#-----------------------------------------------------------------------------

class BaseUpdate(BaseModel):
    update_title: str

class UpdateCreate(BaseUpdate):
    pass

class Update(BaseUpdate):
    update_id: int
    created_by: str
    creation_date: datetime
    revelant_points: Points

#-----------------------------------------------------------------------------

class BaseProject(BaseModel):
    project_name: str
    project_active: bool
    
    class Config:
        orm_mode = True

class ProjectCreate(BaseProject):
    pass

class Project(BaseProject):
    project_id: int
    creation_date: datetime
    created_by: str
    project_updates: list[Update]

#-----------------------------------------------------------------------------

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int

#-----------------------------------------------------------------------------

    