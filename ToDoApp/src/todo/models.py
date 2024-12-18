from database import Base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, Column, Integer, String, DateTime, create_engine, ForeignKey

class User(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(72), unique=True, index=True)
    hashed_password = Column(String(72))
    is_active = Column(Boolean, default=True)
    # todos = relationship("UserTodo", back_populates="user")

class UserTodo(Base):
    __tablename__ = "user_todo"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(256))
    description = Column(String(256))
    time = Column(DateTime)
    email = Column(String(72))
    user_id = Column(Integer, ForeignKey('User.id')) 
    # user = relationship("User", back_populates="todos")