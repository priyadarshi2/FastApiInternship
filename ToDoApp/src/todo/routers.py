from typing import List, Union
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from src.todo.models import UserTodo
from src.todo.schema import PaginatedTaskResponse, TaskCreate, TaskResponse, TaskUpdate
from src.todo.service import save_task, get_all_tasks, get_task_by_id, greet, task_update, task_delete
from database import get_db
from datetime import datetime

router = APIRouter()

#Create database tables
#Base.metadata.create_all(bind=engine)

@router.get("/")
async def root():
    return greet()

@router.post("/tasks/",response_model=TaskResponse)
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    result = save_task(task,db)
    return result

# @router.get("/tasks/{task_id}", response_model=TaskResponse)
# async def get_task_id(task_id: int, db: Session = Depends(get_db)):
#     result = get_task_by_id(task_id,db)
#     return result

@router.get("/tasks/", response_model=Union[TaskResponse,PaginatedTaskResponse])
async def get_tasks(request: Request, db: Session = Depends(get_db)):
    task_id = request.query_params.get('task_id',"")
    page = int(request.query_params.get('page',1))
    page_size =int( request.query_params.get('page_size',10))
    offset = (page - 1) * page_size
    if task_id != "":
        task = get_task_by_id(task_id, db)
        return task # Single task response
    else:
        result,total_count = get_all_tasks(db,offset,page_size) 
        return PaginatedTaskResponse(tasks=result,
            total_count=total_count,
            page=page,
            page_size=page_size)

@router.put("/update/{task_id}", response_model=TaskResponse)
async def update_task( task:TaskUpdate,task_id :int , db: Session = Depends(get_db)):
    db_task = task_update(db, task_id,task)
    if db_task is None: 
        raise HTTPException(status_code=404, detail="Task not found") 
    return db_task

@router.delete("/delete/{task_id}")
async def delete_task(task_id : int, db : Session = Depends(get_db)):
    db_task = task_delete(db, task_id)
    if db_task is None: 
        raise HTTPException(status_code=404, detail="Task not found") 
    return {"message":f"Task ID: {task_id} is deleted succesfully"}



