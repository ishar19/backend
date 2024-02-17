import uuid
from sqlalchemy import (
    TEXT,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    BigInteger

)

from .database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'user'
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    
    
class History(Base):
    __tablename__ = 'history'
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    dateCreated = Column(DateTime, nullable=False)
    user_id = Column(String, ForeignKey('user.id'), nullable=False)
    barcode = Column(BigInteger)

class Product(Base):
    __tablename__ = 'product'
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String)
    allergens= Column(String)
    brands = Column(String)
    carbon_footprint = Column(Integer)
    categories = Column(String)
    countries = Column(String)
    ecoscore_grade = Column(String)
    ecoscore_score = Column(Integer)
    image_url = Column(String)
    ingredients = Column(String)
    nova_group = Column(Integer)
    nutrient_levels = Column(TEXT)
    nutriscore_grade = Column(String)
    nutriscore_score = Column(Integer)
    nutriments = Column(TEXT)
    packaging = Column(String)
    warnings = Column(TEXT)
    
    