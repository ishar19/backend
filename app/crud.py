import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from .models import History
from .database import get_db,SessionLocal
from loguru import logger



def get_db():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

db_gen = get_db()
db = next(db_gen)

def create_new_product(user_id, barcode, db: Session = db):
    logger.debug(f"Creating new barcode for user_id: {user_id}, barcode: {barcode}")
    try:
        new_id = uuid.uuid4()
        new_record = History(id=new_id, dateCreated=datetime.now(), user_id=user_id, barcode=str(barcode))
        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        logger.debug(f"New barcode created: {new_record}")
        return new_id
    except IntegrityError:
        db.rollback()
        raise Exception("Failed to create a new barcode. Integrity constraint violated.")