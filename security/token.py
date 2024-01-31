from typing import Annotated
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta

from .jwt import LoginToken, Token, create_access_token, create_refresh_token, decode_access_token, decode_refresh_token
from business_logic.database.tables import user as bl_user, refresh_token as bl_refresh_token

from business_logic.database.model_dto import User, RefreshToken as BL_RefreshToken

router = APIRouter(
    prefix="/login",
    tags=["tokens"],
    responses={404: {"description": "Not found"}}
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")

class RefreshToken(BaseModel):
    refresh_token: str

@router.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
    ) -> LoginToken:
    user = bl_user.authenticate(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    check_and_delete_refresh_tokens(user.id)

    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    bl_refresh_token.save(user_id=user.id, token=refresh_token)

    return LoginToken(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    user_id = decode_access_token(token)
    if not user_id:
        raise credentials_exception

    user = bl_user.get(user_id)

    if not user:
        raise credentials_exception
    
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
    ):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/refresh")
async def refresh_token(data: RefreshToken):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    user_id = decode_refresh_token(data.refresh_token)
    is_active = bl_refresh_token.is_active(user_id=user_id, token=data.refresh_token)

    if is_active:
        access_token = create_access_token(data={"sub": str(user_id)})
        return Token(access_token=access_token, token_type="bearer")
    try:
        bl_refresh_token.delete(data.refresh_token)
    except:
        pass

    raise credentials_exception

def check_and_delete_refresh_tokens(user_id: int):
    tokens = bl_refresh_token.get_all(user_id)

    for i in tokens:
        result = decode_refresh_token(i.token)
        if not result:
            bl_refresh_token.delete(i.token)


@router.post("/get")
async def get_all_refresh_tokens(
    current_user: Annotated[User, Depends(get_current_active_user)],
    data: RefreshToken) -> list[BL_RefreshToken]:
    tokens = bl_refresh_token.get_all_for_user(current_user.id, data.refresh_token)
    return tokens

class Choice(BaseModel):
    tokens: list[int]

@router.post("/delete")
async def delete(
    current_user: Annotated[User, Depends(get_current_active_user)],
    data: Choice) -> list[int]:
    return bl_refresh_token.delete_many(current_user.id, data.tokens)
