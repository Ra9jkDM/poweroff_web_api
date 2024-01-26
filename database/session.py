from functools import wraps
from sqlalchemy.orm import Session
from database.model import ENGINE


def session(func):
    @wraps(func)
    def create_session(*args, **kwargs):
        with Session(autoflush=True, bind=ENGINE) as db:
            return func(db, *args, **kwargs)
    
    return create_session
