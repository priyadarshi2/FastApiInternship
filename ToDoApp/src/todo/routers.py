from typing import List, Union
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from src.todo.models import UserTodo, User
from src.todo.schema import PaginatedTaskResponse, TaskCreate, TaskResponse, TaskUpdate, Token, UserCreate, UserResponse, UserID
from src.todo.service import save_task, get_all_tasks, get_task_by_id, greet, task_update, task_delete, search_in_title, authenticate_user, get_current_user, get_user
from database import get_db
from datetime import datetime
from fastapi.security import OAuth2PasswordRequestForm
from src.utils import create_access_token, get_password_hash

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
    search_for = request.query_params.get('search_for',"")
    offset = (page - 1) * page_size
    if task_id != "":
        task = get_task_by_id(task_id, db)
        return task # Single task response
    if search_for != "":
        searched_tasks,total_count = search_in_title(db, search_for)
        return PaginatedTaskResponse(tasks=searched_tasks,
            total_count=total_count,
            page=page,
            page_size=page_size)
        # return TitleTaskSearchResponse(task = searched_tasks)
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


@router.get("/me", response_model=UserID)
def read_users_me(current_user: UserID = Depends(get_current_user)):
     return current_user

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
     user = authenticate_user(db, form_data.username, form_data.password)
     if not user:
         raise HTTPException(
             status_code=status.HTTP_401_UNAUTHORIZED,
             detail="Incorrect username or password",
             headers={"WWW-Authenticate": "Bearer"},
         )
     access_token = create_access_token(data={"sub": user.username})
     return {"access_token": access_token, "token_type": "bearer"}

@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    print("============>")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
