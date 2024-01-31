from typing import Annotated
from fastapi import APIRouter, Depends
import security.token as token
from business_logic.database.model_dto import User

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}}
)

@router.get("/", response_model=User)
async def get_user_info(
    current_user: Annotated[User, Depends(token.get_current_active_user)]):
    return current_user

@router.get("/active")
async def is_active(
    current_user: Annotated[User, Depends(token.get_current_active_user)]):
    return True

# /create
# /delete
# /change_password