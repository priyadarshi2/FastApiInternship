from typing import List, Union
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from src.todo.models import UserTodo, User
from src.todo.schema import PaginatedTaskResponse, TaskCreate, TaskResponse, TaskUpdate, Token, UserCreate, UserResponse, UserID, EmailSchema
from database import get_db
from datetime import datetime
from fastapi.security import OAuth2PasswordRequestForm
from src.utils import create_access_token, get_password_hash
import src.todo.service as srv
from src.email_config import conf
from fastapi_mail import MessageSchema, FastMail
from apscheduler.schedulers.background import BackgroundScheduler  # runs tasks in the background
from apscheduler.triggers.cron import CronTrigger  # allows us to specify a recurring time for ex
from database import SessionLocal

router = APIRouter()

@router.get("/")
async def root():
    return srv.greet()

@router.post("/tasks/",response_model=TaskResponse)
async def create_task(task: TaskCreate, db: Session = Depends(get_db), current_user: UserID = Depends(srv.get_current_user)):
    print("curr ---- user--->",current_user.id)

    #print("task===>",task)
    #print("task-title===>",task.title)

    # raise Exception("all well")
    
    result = srv.save_task(task,db,current_user.id)

    return result


# @router.get("/tasks/", response_model=Union[TaskResponse,PaginatedTaskResponse])
# # async def get_tasks(request: Request, db: Session = Depends(get_db)):
# #     task_id = request.query_params.get('task_id',"")
# #     page = int(request.query_params.get('page',1))
# #     page_size =int( request.query_params.get('page_size',10))
# #     search_for = request.query_params.get('search_for',"")
# #     offset = (page - 1) * page_size
# #     if task_id != "":
# #         task = srv.get_task_by_id(task_id, db)
# #         return task # Single task response
# #     if search_for != "":
# #         searched_tasks,total_count = srv.search_in_title(db, search_for)
# #         return PaginatedTaskResponse(tasks=searched_tasks,
# #             total_count=total_count,
# #             page=page,
# #             page_size=page_size)
# #         # return TitleTaskSearchResponse(task = searched_tasks)
# #     else:
# #         result,total_count = srv.get_all_tasks(db,offset,page_size) 
# #         return PaginatedTaskResponse(tasks=result,
# #             total_count=total_count,
# #             page=page,
# #             page_size=page_size)
    
# @router.get("/users/tasks", response_model=List[TaskResponse])
# async def get_tasks_users(db : Session = Depends(get_db), current_user: UserID = Depends(srv.get_current_user)):
#     user_id = current_user.id
#     tasks = srv.tasks_by_user(user_id, db)
#     return tasks

@router.get("/users/tasks/", response_model=Union[TaskResponse,PaginatedTaskResponse])
async def get_tasks(request: Request, db: Session = Depends(get_db), current_user : UserID = Depends(srv.get_current_user)):
    user_id = current_user.id
    print("user-id==>",user_id)
    page = int(request.query_params.get('page',1))
    page_size =int( request.query_params.get('page_size',10))
    search_for = request.query_params.get('search_for',"")
    offset = (page - 1) * page_size
    # if user_id != None:
    #     task = srv.tasks_by_user(user_id, db)
    #     return task # Single task response
    if search_for != "":
        searched_tasks,total_count = srv.search_in_title(db, search_for)
        return PaginatedTaskResponse(tasks=searched_tasks,
            total_count=total_count,
            page=page,
            page_size=page_size)
    else:
        print("============POint1==============")
        result,total_count = srv.tasks_by_user(user_id,offset,page_size,db) 
        print("=============Point2============")
        return PaginatedTaskResponse(tasks=result,
            total_count=total_count,
            page=page,
            page_size=page_size)
    
@router.put("/update/{task_id}", response_model=TaskResponse)
async def update_task( task:TaskUpdate,task_id :int , db: Session = Depends(get_db)):
    db_task = srv.task_update(db, task_id,task)
    if db_task is None: 
        raise HTTPException(status_code=404, detail="Task not found") 
    return db_task

@router.put("/user/update/{task_id}", response_model=TaskResponse)
async def update_task_user( task:TaskUpdate, task_id :int , db: Session = Depends(get_db), current_user : UserID = Depends(srv.get_current_user)):
    user_id = current_user.id
    db_task = srv.task_update_user(db, task_id,task, user_id)
    if db_task is None: 
        raise HTTPException(status_code=404, detail="Task not found") 
    return db_task

@router.delete("/delete/{task_id}")
async def delete_task(task_id : int, db : Session = Depends(get_db)):
    db_task = srv.task_delete(db, task_id)
    if db_task is None: 
        raise HTTPException(status_code=404, detail="Task not found") 
    return {"message":f"Task ID: {task_id} is deleted succesfully"}

@router.delete("/user/delete/{task_id}")
async def delete_task_user(task_id : int, db : Session = Depends(get_db), current_user : UserID = Depends(srv.get_current_user)):
    user_id = current_user.id
    db_task = srv.task_delete_user(db, task_id, user_id)
    if db_task is None: 
        raise HTTPException(status_code=404, detail="Task not found") 
    return {"message":f"Task ID: {task_id} is deleted succesfully"}

    
@router.get("/me", response_model=UserID)
def read_users_me(current_user: UserID = Depends(srv.get_current_user)):
     return current_user

@router.post("/token")
def login_for_access_token(form_data: UserCreate, db: Session = Depends(get_db)):
     user = srv.authenticate_user(db, form_data.username, form_data.password)
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
    db_user = srv.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    print("============>")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/trigger/") 
async def startup_event(): 
    with SessionLocal() as session: 
        tasks = session.query(UserTodo).all() 
        for task in tasks: 
            srv.schedule_task_email(task)

@router.post("/send-email/")
async def send_email_endpoint(email: EmailSchema, template: str): 
    await srv.send_email(email.email, "Task Reminder", template) 
    return {"message": "Email sent successfully"}