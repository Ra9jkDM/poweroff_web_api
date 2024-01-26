from __future__ import annotations
from typing import List
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, Float, String, Date, DateTime, ForeignKey, select, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship, mapped_column, Mapped, relationship, backref

from security.hash import hash_password
from os import environ

USERNAME = environ.get("database_username") 
PASSWORD = environ.get("database_password")

HOST = environ.get("database_host")
PORT = int(environ.get("database_port"))

DATABASE = environ.get("database_name")
DIALECT = environ.get("database_dialect")


ENGINE = create_engine(f"{DIALECT}://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}") #, echo=True)
Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, autoincrement=True)
    username: Mapped[String] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[String] = mapped_column(String(150), nullable=False)
    disabled: Mapped[Boolean] = mapped_column(Boolean, default=False, nullable=False)

    refresh_tokens: Mapped[List["RefreshToken"]] = relationship()

class RefreshToken(Base):
    __tablename__ = "refresh_token"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    
    token: Mapped[String] = mapped_column(String(1000), nullable=False)
    creation_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="refresh_tokens")



def create_user(username, password):
    with Session(autoflush=True, bind=ENGINE) as db:
        user = User(username=username, password=hash_password(password))
        db.add(user)
        db.commit()



def create_db():
    Base.metadata.create_all(bind=ENGINE)


def delete_db():
    Base.metadata.drop_all(bind=ENGINE)

if __name__ == "__main__":
    # delete_db()
    create_db()
    create_user("bob", "pwd123")

# python -m database.model