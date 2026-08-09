from sqlalchemy.orm import Session

from backend.app.crud.user import (
    create_user,
    get_user_by_email,
    get_user_by_username,
)
from backend.app.schemas.user import UserCreate


def register_user(db: Session, user: UserCreate):

    if get_user_by_email(db, user.email):
        raise ValueError("Email already registered.")

    if get_user_by_username(db, user.username):
        raise ValueError("Username already exists.")

    return create_user(db, user)
