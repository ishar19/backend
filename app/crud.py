import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from .models import History,Product
from .database import db
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from sqlalchemy import desc

def update_history(user_id, barcode, db: Session = db):
    logger.debug(f"History:- Creating new barcode for user_id: {user_id}, barcode: {barcode}")
    try:
        new_id = uuid.uuid4()
        new_record = History(id=new_id, dateCreated=datetime.now(), user_id=user_id, barcode=str(barcode))
        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        logger.debug(f"History:- New barcode created: {new_record}")
        return new_id
    except IntegrityError:
        db.rollback()
        raise HTTPException("History:- Failed to create a new barcode. Integrity constraint violated.")

def create_product_from_response(product: dict, db: Session = db):
    
    existing_product = get_product(product.get('_id'), db)
    if existing_product:
        logger.debug(f"Product with ID {product.get('id')} already exists. Skipping creation.")
        return existing_product
    
    logger.debug(f"Creating new product for barcode: {product.get('_id')}")
    new_product = Product(  
        id=product.get('_id'),
        name=product.get('product_name'),
        image_url=product.get('image_url'),
        allergens=product.get('allergens'),
        brands=product.get('brands'),
        carbon_footprint=product.get('carbon_footprint_percent_of_known_ingredients'),
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

def get_product(product_id: int, db: Session = db):
    logger.debug(f"Fetching product with ID {product_id}")
    return db.get(Product, product_id)

def fetch_history(user_id: int, db: Session = db):
    try:
        history_records = db.query(History).filter(History.user_id == user_id).order_by(desc(History.dateCreated)).all()
        result = [{"id": record.id, "barcode": record.barcode} for record in history_records]
        return result
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error occurred")