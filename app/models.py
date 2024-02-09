import uuid
from sqlalchemy import (
    TEXT,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,

)

from .database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class History(Base):
    __tablename__ = 'history'
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    dateCreated = Column(DateTime, nullable=False)
    user_id = Column(Integer)
    barcode = Column(String)
    
    