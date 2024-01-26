from datetime import datetime

from ..session import session
from ..model import User, RefreshToken


@session
def get(db, user_id: int, token: str):
    return db.query(RefreshToken).filter(RefreshToken.user_id==user_id, RefreshToken.token==token).first()

@session
def get_all(db, user_id: int):
    return db.query(RefreshToken).filter(RefreshToken.user_id==user_id).all()

@session
def save(db, user_id: int, token: str):
    token = RefreshToken(user_id=user_id, token=token, creation_date=datetime.now())
    db.add(token)
    db.commit()

@session
def delete(db, token: str):
    token = db.query(RefreshToken).filter(RefreshToken.token==token).first()
    db.delete(token)
    db.commit()

