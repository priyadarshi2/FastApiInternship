from database import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, Column, Integer, String, DateTime, create_engine

class UserTodo(Base):
    __tablename__ = "user_todo"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(48))
    description = Column(String(256))
    time = Column(DateTime)
    email = Column(String(72))



