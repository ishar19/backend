from ..database import get_db
from fastapi import APIRouter
from loguru import logger
from typing import Dict
from fastapi import Depends
from fastapi import  HTTPException, status
from ..models import User
from sqlalchemy.orm import Session
from ..schemas.user import UserCreate
from sqlalchemy.exc import IntegrityError

user_router = APIRouter(
  prefix='/user',
  tags=['User CRUD']
)

@user_router.post("/create")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    logger.debug(f"Creating new user: {user}")
    new_user = User(id =user.id,name=user.name, email=user.email, image_url = user.image_url)
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    finally:
        db.close()
