import traceback

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.schemas.user import UserCreate
from backend.app.services.user_service import register_user

router = APIRouter()


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return register_user(db, user)
    except Exception as error:
        return JSONResponse(
            status_code=500,
            content={
                "error_type": type(error).__name__,
                "error": str(error),
                "traceback": traceback.format_exc(),
            },
        )
