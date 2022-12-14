from fastapi import FastAPI
from .routers import project, user, auth
from . import models
from .database import engine

models.Base.metadata.create_all(bind = engine)

app = FastAPI()
app.include_router(project.router)
app.include_router(user.router)
app.include_router(auth.router)
