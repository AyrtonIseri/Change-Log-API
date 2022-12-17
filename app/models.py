from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, ARRAY
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class Projects(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, nullable = False)
    title = Column(String, nullable=False)
    active = Column(Boolean, server_default='TRUE', nullable=False)
    creation_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("Users")

class Users(Base):
    __tablename__ = "users"

    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    id = Column(Integer, primary_key=True, nullable=False)
    creation_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))

class Updates(Base):
    __tablename__ = "updates"

    id = Column(Integer, primary_key=True, nullable = False)
    title = Column(String, nullable=False)
    creation_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

class Points(Base):
    __tablename__ = "points"

    id = Column(Integer, primary_key = True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(ARRAY(String), nullable=True)

class ProjToUpdates(Base):
    __tablename__ = "proj_update"

    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    update_id = Column(Integer, ForeignKey("updates.id", ondelete="CASCADE"), nullable=False)

class UpdateToPoints(Base):
    __tablename__ = "update_point"

    update_id = Column(Integer, ForeignKey("updates.id", ondelete="CASCADE"), nullable=False)
    point_id = Column(Integer, ForeignKey("points.id", ondelete="CASCADE"), nullable=False)