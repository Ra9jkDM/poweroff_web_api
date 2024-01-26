import database.tables.user as User
import database.tables.refresh_token as refresh_token
import database.converter as convert

from .hash import verify_password

def authenticate_user(username: str, password: str):
    user = User.get(username)

    if not user:
        return False
    if not verify_password(password, user.password):
        return False

    return convert.user(user)

def get_user(user_id: str):
    user = User.get_by_id(int(user_id))
    return convert.user(user)


def save_refresh_token(user_id: int, token: str):
    refresh_token.save(user_id, token)

def delete_refresh_token(token: str):
    refresh_token.delete(token)

def is_refresh_token_active(user_id: str, token: str):
    token = refresh_token.get(int(user_id), token)

    if token:
        return True
    return False

def refresh_token_get_all(user_id: int):
    return refresh_token.get_all(user_id)