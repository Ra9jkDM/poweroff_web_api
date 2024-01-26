from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    id: int
    username: str
    password: str
    disabled: bool

class RefreshToken(BaseModel):
    id: int
    creation_date: datetime
    current: bool = False
