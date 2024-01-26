from .model_dto import *

def user(user):
    return User(
        id=user.id,
        username=user.username, 
        password="",
        disabled=user.disabled)

def refresh_token(token):
    return RefreshToken(
        id=token.id,
        creation_date=token.creation_date)