from database import get_db
from src.todo.models import UserTodo
from src.todo.schema import TaskCreate, TaskResponse
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder

def greet():
    return {"message": "welcome to to do app"}

def save_task(task,db):
    db_task = UserTodo(
        title=task.title,
        description=task.description,
        time=task.time,
        email=task.email
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_task_by_id(task_id, db):
    task = db.query(UserTodo).filter(UserTodo.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

def get_all_tasks(db,offset,limit):
    # total = db.query(ItemModel).count()
    tasks = db.query(UserTodo).offset(offset).limit(limit).all()
    total_count = db.query(UserTodo).count()
    return tasks,total_count

def task_update(db, task_id,task):
    db_task = db.query(UserTodo).filter(UserTodo.id == task_id).first() 
    if db_task: 
       db_task.title = task.title
       db_task.description = task.description
       db_task.time = task.time
       db_task.email = task.email
    db.commit() 
    db.refresh(db_task) 
    return db_task

def task_delete(db, task_id):
    db_task = db.query(UserTodo).filter(UserTodo.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task