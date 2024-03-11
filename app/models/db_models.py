from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime
from sqlalchemy.dialects.mysql import CHAR, LONGTEXT
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
import json

Base = declarative_base()

class Memory(Base):
    __tablename__ = 'memories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(CHAR(36), nullable=False)
    name = Column(String(255))
    content = Column(Text)
    reflection = Column(Text)
    tags = Column(LONGTEXT)
    active = Column(Boolean, default=True)
    source = Column(String(255))
    created_at = Column(DateTime, default=func.now())
