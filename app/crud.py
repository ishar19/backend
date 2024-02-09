import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from .models import History
from .database import get_db


def create_new_product(user_id, barcode,db: Session = Depends(get_db.asend(None))):
    try:
        new_id = uuid.uuid4()
        new_record = History(id=new_id, dateCreated=datetime.now(), user_id=user_id, barcode=barcode)
        db.add(new_record)
        db.commit()
        return new_id
    except IntegrityError:
        db.rollback()
        raise Exception("Failed to create a new barcode. Integrity constraint violated.")