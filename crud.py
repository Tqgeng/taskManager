# операции с бд

from sqlalchemy.orm import Session
from shemas import TaskCreate, TaskUpdate, TaskUpdated
import models
from auth.utils import hash_password

def get_tasks(db: Session, user_id: int):
    return db.query(models.Task).filter(models.Task.owner_id == user_id).all()

def get_task(db: Session, id: int):
    return db.query(models.Task).filter(models.Task.id == id).first()

def create_task(db: Session, task: TaskCreate, user_id: int):
    new_task = models.Task(title = task.title, description = task.description, owner_id = user_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def update_task(db: Session, task: TaskUpdate, id: int):
    task_ = db.query(models.Task).filter(models.Task.id == id).first()
    task_.title = task.title
    task_.description = task.description
    # task_.completed = task.completed
    db.commit()
    db.refresh(task_)
    return task_

def update_task_status(db: Session, task: TaskUpdated, id: int):
    task_ = db.query(models.Task).filter(models.Task.id == id).first()
    task_.completed = task.completed
    db.commit()
    db.refresh(task_)
    return task_

def delete_task(db: Session, id: int):
    task = db.query(models.Task).filter(models.Task.id == id).first()
    db.delete(task)
    db.commit()
    return task

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, username: str, hashed_password: str, email: str = None):
    db_user = models.User(
        username = username,
        password = hashed_password,
        email = email,
        
    )   
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_text_user(db: Session, username: str, hashed_password: str, email: str = None):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    db_user.username = username
    if email:
        db_user.email = email
    
    db_user.password = hashed_password

    db.commit()
    db.refresh(db_user)

    return db_user
