from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, JSON, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from enum import Enum
from sqlalchemy.dialects.mysql import CHAR, LONGTEXT
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

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

class ConversationStatus(Enum):
    ACTIVE = "active"
    CLOSED = "closed"
    ARCHIVED = "archived" 

class MessageRole(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class ConversationModel(Base):
    __tablename__ = 'conversations'
    
    id = Column(CHAR(36), primary_key=True)  # UUID
    title = Column(String(255))
    status = Column(SQLEnum(ConversationStatus, values_callable=lambda obj: [e.value for e in obj]), default=ConversationStatus.ACTIVE)
    meta_data = Column(JSON)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    messages = relationship("ConversationMessageModel", back_populates="conversation", cascade="all, delete-orphan")

class ConversationMessageModel(Base):
    __tablename__ = 'conversation_messages'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(CHAR(36), ForeignKey('conversations.id', ondelete='CASCADE'), nullable=False)
    role = Column(SQLEnum(MessageRole), nullable=False)
    content = Column(Text, nullable=False)
    meta_data = Column(JSON)
    created_at = Column(DateTime, default=func.now())
    
    # Relationship back to conversation
    conversation = relationship("ConversationModel", back_populates="messages")