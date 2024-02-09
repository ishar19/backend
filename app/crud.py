import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from .models import History,Product
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

def update_history(user_id, barcode, db: Session = db):
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

def create_product(product, db: Session = db):
    logger.debug(f"Creating new product for barcode: {product.get('id')}")
    
    existing_product = db.query(Product).filter(Product.id == product.get('id')).first()
    if existing_product:
        logger.debug(f"Product with ID {product.get('id')} already exists. Skipping creation.")
        return existing_product

    new_product = Product(  
        id=product.get('id'),
        name=product.get('product_name'),
        image_url=product.get('image_url'),
        allergens=product.get('allergens'),
        brands=product.get('brands'),
        categories=product.get('categories'),
        countries=product.get('countries'),
        ecoscore_grade=product.get('ecoscore_grade'),
        ecoscore_score=product.get('ecoscore_score'),
        ingredients=product.get('ingredients_text_en'),
        nova_group=product.get('nova_group'),
        nutrient_levels=str(product.get('nutrient_levels') or {}),
        nutriments=str(product.get('nutriments') or {}),
        nutriscore_grade=product.get('nutriscore_grade'),
        nutriscore_score=product.get('nutriscore_score'),
        packaging=product.get('packaging_text_en'),
        warnings=str(product.get('ecoscore_extended_data', {}).get('impact', {}).get('warnings') or [])
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product
