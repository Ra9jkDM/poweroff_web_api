from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

import security.token as token

from business_logic.database.model_dto import User

app = FastAPI()

app.include_router(token.router)

def allow_cross_origin_requests():
    origins = [
        "http://localhost:4200",
        "http://localhost:8080",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(token.get_current_active_user)]):
    return current_user

if __name__ == "__main__":
    allow_cross_origin_requests()