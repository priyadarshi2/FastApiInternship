from database import get_db
from src.todo.models import UserTodo,User
from src.todo.schema import TaskCreate, TaskResponse, TokenData, UserID
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from src.utils import verify_password
from fastapi import Depends, HTTPException, Header, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from src.utils import SECRET_KEY, ALGORITHM
from sqlalchemy import and_
from datetime import datetime
from fastapi_mail import MessageSchema
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from src.email_config import fm
import asyncio

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def greet():
    return {"message": "welcome to to do app"}

def save_task(task,db,curr_user_id):
    db_task = UserTodo(
        title=task.title,
        description=task.description,
        time=task.time,
        email=task.email,
        user_id = curr_user_id
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
    total_task = db.query(UserTodo).filter()
    tasks = total_task.offset(offset).limit(limit)
    total_count = total_task.count()

    # total_count = db.query(UserTodo).count()
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

def task_update_user(db, task_id,task, user_id):
    db_task = db.query(UserTodo).filter(and_(UserTodo.id == task_id, UserTodo.user_id == user_id)).first() 
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

def task_delete_user(db, task_id, user_id):
    db_task = db.query(UserTodo).filter(and_(UserTodo.id == task_id, UserTodo.user_id == user_id)).first()
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task

def search_in_title(db, text):
    db_task = db.query(UserTodo).filter(UserTodo.title.icontains(text))
    total_count = db_task.count()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    else :
        return db_task,total_count

def get_user(db: Session, username: str):
    if username == "":
        raise HTTPException(status_code=422, detail="Username Can't be empty")
    else:
        return db.query(User).filter(User.username == username).first()


def authenticate_user(db, username, password):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# def get_current_user(token, db : Session = Depends(get_db)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     user = get_user(db, username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user
def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    print("authoiration==>",authorization)
    if not authorization:
        raise credentials_exception
    
    token = authorization.split("Bearer ")[-1] if "Bearer " in authorization else authorization

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    
    return user


def tasks_by_user(user_id : int, offset, page_size,db : Session = Depends(get_db)):
    if user_id == None:
        raise HTTPException(status_code=422, detail="Username Can't be empty")
    else:
        user_tasks = db.query(UserTodo).filter(UserTodo.user_id == user_id)
        tasks = user_tasks.offset(offset).limit(page_size)
        total_count = user_tasks.count()
    return tasks,total_count

def is_user_active(user_id : int, db : Session = Depends(get_db)):
    result = db.query(User.is_active).join(UserTodo).filter(and_(User.id == user_id, UserTodo.user_id == user_id)).first() 
    return result

def save_task_user(task, user_id : int, db : Session = Depends(get_db) ):
    db_task = UserTodo(
        title=task.title,
        description=task.description,
        time=task.time,
        email=task.email,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def current_time_greet():
    print(f"Task is running at {datetime.now()}")

async def send_email(to: str, subject: str, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=[to],
        body=body,
        subtype="html"
    )
    try: 
        await fm.send_message(message) 
        print(f"Email sent to {to} at {datetime.now()}") 
    except Exception as e: # Log the error and raise an HTTPException 
        print(f"Failed to send email: {e}") 
        raise HTTPException(status_code=400, detail=f"Failed to send email: {e}")

def schedule_task_email(task):

    # Scheduler setup
    scheduler = BackgroundScheduler()
    scheduler.start()
    # Calculate the time difference
    task_time = task.time
    current_time = datetime.now()
    time_difference = task_time - current_time

    # Ensure the task is scheduled in the future
    if time_difference.total_seconds() > 0:
        scheduler.add_job(send_email_wrapper, 
                          DateTrigger(run_date=task_time),
                          args=[task.email, "Task Reminder", task.description])

def send_email_wrapper(to, subject, body): 
    asyncio.run(send_email(to, subject, body))