from typing import Annotated
from fastapi import APIRouter, Depends
import os
import security.token as token
from business_logic.database.model_dto import User

router = APIRouter(
    prefix="/power",
    tags=["power"],
    responses={404: {"description": "Not found"}}
)

@router.get("/reboot")
async def reboot(
    current_user: Annotated[User, Depends(token.get_current_active_user)]):
    os.system("echo rebooting...")
    return True

@router.get("/shutdown")
async def shutdown(
    current_user: Annotated[User, Depends(token.get_current_active_user)]):
    os.system("echo shutdown...")
    return True

# /create
# /delete
# /change_password

# /power/shutdown
# /power/reboot