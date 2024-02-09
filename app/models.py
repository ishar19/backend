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

class History(Base):
    __tablename__ = 'history'
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    dateCreated = Column(DateTime, nullable=False)
    user_id = Column(Integer)
    barcode = Column(BigInteger)

class Product(Base):
    __tablename__ = 'product'
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String)
    allergens= Column(String)
    brands = Column(String)
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
    
    