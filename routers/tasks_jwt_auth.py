from __future__ import annotations

from jwt.exceptions import InvalidTokenError
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from auth import utils as auth_utils
from typing import Union
from sqlalchemy.orm import Session
import crud

from database import SessionLocal
from shemas import UserShema, UserCreate
from pydantic import BaseModel

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# http_bearer = HTTPBearer()
oauth2_sheme = OAuth2PasswordBearer(tokenUrl='/jwt/login/',)

class TokenInfo(BaseModel):
    access_token: str
    token_type: str

router = APIRouter(prefix='/jwt', tags=['JWT'])

# nick = UserShema(
#     username='nick',
#     password=auth_utils.hash_password('qwerty'),
#     email='nick@example.com'
# )

# andre = UserShema(
#     username='andre',
#     password=auth_utils.hash_password('secret')
# )

# users_db: dict[str, UserShema] = {
#     nick.username: nick,
#     andre.username: andre
# }

def validate_auth_user(
        username: str = Form(),
        password: str = Form(),
        db: Session = Depends(get_db)
):
    unauthed_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail = 'Invalid username or password')
    
    # if not (user:= users_db.get(username)):
    #     raise unauthed_exception

    user = crud.get_user_by_username(db, username)
    
    # if not auth_utils.validate_password(
    #     password=password, 
    #     hashed_password=user.password
    # ):
    #     raise unauthed_exception

    if not user or not auth_utils.validate_password(
        password, user.password
    ):
        raise unauthed_exception

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail = 'user inactive'
        )  
    return user
    

@router.post('/login/', response_model=TokenInfo)
def auth_user_issue_jwt(
    user: UserShema = Depends(validate_auth_user)
):
    jwt_payload = {
        'sub': user.username,
        'username': user.username,
        'email': user.email,
        # 'logged_in_at' 
    }
    access_token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=access_token,
        token_type='Bearer'
    )

def get_current_token_payload(
        # credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
        token: str = Depends(oauth2_sheme)
) -> dict:
    # token = credentials.credentials
    try:
        payload = auth_utils.decode_jwt(
            token=token
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'invalid token error {e}'
        )
    return payload

def get_current_auth_user(
        payload: dict = Depends(get_current_token_payload),
        db: Session = Depends(get_db)
) -> UserShema:
        username: Union[str, None] = payload.get('sub')
        user = crud.get_user_by_username(db, username)
        if user:
            return user
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='token invalid (user not found)'
        )


def get_current_active_auth_user(
        user: UserShema = Depends(get_current_auth_user)
):
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='user inactive'
    )

@router.get('/users/me')
def auth_user_check_self_info(
    payload: dict = Depends(get_current_token_payload),
    user: UserShema = Depends(get_current_active_auth_user)
):
    iat = payload.get('iat')
    return {
        'username': user.username,
        'email': user.email,
        'logged_in_at': iat
    }

@router.post('/register', response_model=UserCreate)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    ex_user = crud.get_user_by_username(db, user_data.username)
    if ex_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Username already taken'
        )
    
    hashed_password = auth_utils.hash_password(user_data.password)

    new_user = crud.create_user(db, user_data.username, hashed_password, user_data.email)

    return UserCreate(
        username=new_user.username,
        password='hidden',
        email=new_user.email
    )

@router.put('/register/status', response_model=UserCreate)
def update_stats_user(user_data: UserCreate, db: Session = Depends(get_db)):
    ex_user = crud.get_user_by_username(db, user_data.username)
    if not ex_user:
        raise HTTPException(
            status_code=status.HTTP_404_BAD_REQUEST,
            detail='Username not found'
        )
    
    hashed_password = auth_utils.hash_password(user_data.password)

    new_user = crud.update_text_user(db, user_data.username, hashed_password, user_data.email)

    return UserCreate(
        username=new_user.username,
        password='hidden',
        email=new_user.email
    )

    
