from ..session import session
from ..model import User

@session
def get(db, username: str):
    return db.query(User).filter(User.username==username).first()

@session
def get_by_id(db, user_id: int):
    return db.query(User).filter(User.id==user_id).first()
