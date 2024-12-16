from database import get_db
from src.todo.models import UserTodo,User
from src.todo.schema import TaskCreate, TaskResponse, TokenData, UserID
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from src.utils import verify_password
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from src.utils import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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

def task_delete(db, task_id):
    db_task = db.query(UserTodo).filter(UserTodo.id == task_id).first()
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
    return db.query(User).filter(User.username == username).first()


def authenticate_user(db, username, password):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def get_current_user(token, db : Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
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
