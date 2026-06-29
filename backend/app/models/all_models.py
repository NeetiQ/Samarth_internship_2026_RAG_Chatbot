import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.database.base import Base

class ProcessingStage(str, enum.Enum):
    UPLOADED = "UPLOADED"
    OCR = "OCR"
    EXTRACTION = "EXTRACTION"
    CLEANING = "CLEANING"
    CHUNKING = "CHUNKING"
    EMBEDDING = "EMBEDDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(50))
    file_path = Column(String(512))
    
    # Structured Metadata
    court = Column(String(255))
    case_number = Column(String(100))
    judgment_date = Column(DateTime)
    source = Column(String(255))
    language = Column(String(50))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    chunks = relationship("Chunk", back_populates="document", cascade="all, delete-orphan")
    processing_jobs = relationship("ProcessingJob", back_populates="document", cascade="all, delete-orphan")

class Chunk(Base):
    __tablename__ = "legal_chunks"
    
    id = Column(Integer, primary_key=True, index=True)
    chunk_id = Column(String(255), unique=True, index=True, nullable=True) # Used by Team B
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=True)
    page_content = Column(Text, nullable=False)
    
    # Team B uses a single JSONB metadata column
    from sqlalchemy.dialects.postgresql import JSONB
    metadata_ = Column("metadata", JSONB, nullable=True)
    
    # PGVector embedding matching Team B's 384 dimensions
    embedding = Column(Vector(384), nullable=True) 
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    document = relationship("Document", back_populates="chunks")
    citations = relationship("Citation", back_populates="chunk")

class ProcessingJob(Base):
    __tablename__ = "processing_jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    stage = Column(Enum(ProcessingStage), default=ProcessingStage.UPLOADED)
    status = Column(String(50), default="pending")  # pending, in_progress, completed, failed
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)

    # Relationships
    document = relationship("Document", back_populates="processing_jobs")

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")
    prompt_logs = relationship("PromptLog", back_populates="session", cascade="all, delete-orphan")

class ChatRole(str, enum.Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False)
    role = Column(Enum(ChatRole), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    session = relationship("ChatSession", back_populates="messages")
    citations = relationship("Citation", back_populates="message", cascade="all, delete-orphan")

class Citation(Base):
    __tablename__ = "citations"
    
    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("chat_messages.id", ondelete="CASCADE"), nullable=False)
    chunk_id = Column(Integer, ForeignKey("legal_chunks.id", ondelete="SET NULL"), nullable=True)
    score = Column(Float)

    # Relationships
    message = relationship("ChatMessage", back_populates="citations")
    chunk = relationship("Chunk", back_populates="citations")

class PromptLog(Base):
    __tablename__ = "prompt_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False)
    prompt_text = Column(Text, nullable=False)
    model = Column(String(100), nullable=False)
    tokens_used = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    session = relationship("ChatSession", back_populates="prompt_logs")
