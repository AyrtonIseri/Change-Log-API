from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class Projects(Base):
    __tablename__ = "project_table"

    project_id = Column(Integer, primary_key=True, nullable = False)
    project_name = Column(String, nullable=False)
    project_active = Column(Boolean, server_default='TRUE', nullable=False)
    created_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("Users")

class Users(Base):
    __tablename__ = "users"

    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    id = Column(Integer, primary_key=True, nullable=False)
    created_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))
