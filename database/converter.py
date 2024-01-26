from .model_dto import User

def user(user):
    return User(
        id=user.id,
        username=user.username, 
        password="",
        disabled=user.disabled
        )