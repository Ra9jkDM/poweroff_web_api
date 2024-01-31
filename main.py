from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

import security.token as token
import routers.user as user
import routers.power_signal_controller as power

from business_logic.database.model_dto import User

app = FastAPI()

app.include_router(token.router)
app.include_router(user.router)
app.include_router(power.router)

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

allow_cross_origin_requests()

