# Роуты для задач

import uuid
from fastapi import APIRouter, Depends,  HTTPException, status, Header, Response, Cookie
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from database import SessionLocal
from shemas import TaskCreate, TaskUpdate, TaskResponse, TaskUpdated, UserShema
from crud import get_tasks, get_task, create_task, update_task, delete_task, update_task_status
from typing import Any, Dict, List
from typing_extensions import Annotated
import secrets
from time import time
from routers.tasks_jwt_auth import get_current_active_auth_user, get_current_auth_user


router = APIRouter(prefix='/tasks', tags=['Задачи'])
router_auth = APIRouter(prefix='/demo_auth', tags=['Demo Auth'])

security = HTTPBasic()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/', response_model=List[TaskResponse], tags=['Задачи'], summary='Получить все задачи')
def read_tasks(db: Session = Depends(get_db), user: UserShema = Depends(get_current_active_auth_user)):
    return get_tasks(db, user_id=user.id)

@router.get('/{id}', response_model=TaskResponse, tags=['Задачи'], summary='Получить конкретную задачу')
def read_task(id: int, db: Session = Depends(get_db)):
    task = get_task(db, id)
    if task is None:
        raise HTTPException(status_code=404, detail='Такой задачи нет')
    return task

@router.post('/', response_model=TaskResponse, tags=['Задачи'], summary='Создать задачу')
def create_new_task(task: TaskCreate, db: Session = Depends(get_db), user: UserShema = Depends(get_current_auth_user)):
    return create_task(db, task, user.id)

@router.put('/{id}', response_model=TaskResponse, tags=['Задачи'], summary='Отредактировать задачу')
def update_ex_task(id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    upd_task = update_task(db, task, id)
    if upd_task is None:
        raise HTTPException(status_code=404, detail='Такой задачи нет')
    return upd_task

@router.put('/{id}/status', response_model=TaskResponse, tags=['Задачи'], summary='Отредактировать статус задачи')
def upd_stat_task(id: int, task: TaskUpdated, db: Session = Depends(get_db)):
    upd_st_task = update_task_status(db, task, id)
    if upd_st_task is None:
        raise HTTPException(status_code=404, detail='Такой задачи нет')
    return upd_st_task

@router.delete('/{id}', tags=['Задачи'], summary='Удалить задачу')
def delete_ex_task(id: int, db: Session = Depends(get_db)):
    del_task = delete_task(db, id)
    if del_task is None:
        raise HTTPException(status_code=404, detail='Такой задачи нет')
    return {'message': 'Задача удалена'}

@router_auth.get('/basic-auth/')
def demo_basic_auth_credentials(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    return {'message': 'Hi!',
            'Username': credentials.username,
            'password': credentials.password}

user_name_to_passwords = {
    'admin': 'admin',
    'john' : '12345'
}

def get_auth_user_username(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)]
) -> str:
    unauther_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid username or password', 
        headers={"WWW-Authenticate": "Basic"}
    )

    correct_password = user_name_to_passwords.get(credentials.username)
    if correct_password is None:
        raise unauther_exc
    
    if credentials.username not in user_name_to_passwords:
        raise unauther_exc
    
    if not secrets.compare_digest(
        credentials.password.encode('utf-8'), 
        correct_password.encode('utf-8')
    ):
        raise unauther_exc

    return credentials.username

@router_auth.get('/basic-auth-username/')
def demo_basic_auth_username(
    auth_username: str = Depends(get_auth_user_username)
):
    return {'message': f'Hi! {auth_username}',
            'Username': auth_username
            }

static_auth_token_to_username = {
    '4e3a87eb215b962d9d01d01600605d': 'admin',
    'f170ba19045a72011dc09b48975cfad316' : 'john'
}

def get_username_by_static_auth_token(
        auth_token: str = Header(alias='x-auth-token'),
) -> str:
    # if auth_token not in static_auth_token_to_username: 
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail='Token invalid'
    #     )
    
    # return static_auth_token_to_username[auth_token]
    if username := static_auth_token_to_username.get(auth_token):
        return username
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token invalid'
        )

@router_auth.get('/some-http-header-auth/')
def demo_auth_some_http_header(
    username: str = Depends(get_username_by_static_auth_token)
):
    return {'message': f'Hi! {username}',
            'Username': username
            }

COOKIES: Dict[str, Dict[str, Any]] = {}
COOKIES_SESSION_ID_KEY = 'web-app-session-id'

def generate_session_id() -> str:
    return uuid.uuid4().hex

def get_session_data(
        session_id: str = Cookie(alias=COOKIES_SESSION_ID_KEY)
) -> dict:
    if session_id not in COOKIES:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Not authenticated'
        )
    return COOKIES[session_id]

@router_auth.post('/login-cookie/')
def demo_auth_login_set_cookie(
    response: Response,
    username: str = Depends(get_username_by_static_auth_token)
    # auth_username: str = Depends(get_auth_user_username)
):
    session_id = generate_session_id()
    COOKIES[session_id] = {
        'username' : username,
        'login_at': int(time())
    }
    response.set_cookie(COOKIES_SESSION_ID_KEY, session_id)
    return {'result' : 'ok'}
    
@router_auth.get('/check-cookie/')
def demo_auth_check_cookie(
    user_session_data: dict = Depends(get_session_data)
):
    username = user_session_data['username']
    return {'message': f'hello {username}',
            **user_session_data}

@router_auth.get('/logout-cookie/')
def demo_auth_logout_cookie(
    response: Response,
    session_id: str = Cookie(alias=COOKIES_SESSION_ID_KEY),
    user_session_data: dict = Depends(get_session_data)
):
    COOKIES.pop(session_id)
    response.delete_cookie(COOKIES_SESSION_ID_KEY)
    username = user_session_data['username']
    return {'message': f'Bye {username}'}


