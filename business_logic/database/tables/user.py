import database.tables.user as User
import business_logic.database.converter as convert

from security.hash import verify_password

def authenticate(username: str, password: str):
    user = User.get(username)

    if not user:
        return False
    if not verify_password(password, user.password):
        return False

    return convert.user(user)

def get(user_id: str):
    user = User.get_by_id(int(user_id))
    return convert.user(user)

