from sqlalchemy import Column, String, Boolean, Integer, Float, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="user", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    documents = relationship("Document", back_populates="user")


class Document(Base):
    __tablename__ = "documents"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    title = Column(String(512), nullable=True)
    storage_path = Column(String(1024), nullable=False)
    language = Column(String(32), nullable=True)
    num_words = Column(Integer, nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_reference = Column(Boolean, default=False, nullable=False)

    user = relationship("User", back_populates="documents")


class Job(Base):
    __tablename__ = "jobs"

    id = Column(String(64), primary_key=True)  # celery task id
    document_id = Column(String(36), ForeignKey("documents.id"), nullable=False)
    status = Column(String(32), default="pending", nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    result_path = Column(String(1024), nullable=True)


class Source(Base):
    __tablename__ = "sources"

    id = Column(String(36), primary_key=True)
    title = Column(String(512), nullable=True)
    storage_path = Column(String(1024), nullable=False)
    metadata = Column(JSON, nullable=True)


class Fragment(Base):
    __tablename__ = "fragments"

    id = Column(String(36), primary_key=True)
    job_id = Column(String(64), ForeignKey("jobs.id"), nullable=False)
    doc_pos = Column(Integer, nullable=False)
    length_tokens = Column(Integer, nullable=False)
    matched_source_id = Column(String(36), ForeignKey("sources.id"), nullable=True)
    match_type = Column(String(32), nullable=False)  # exact | fingerprint | lexical | semantic
    score = Column(Float, nullable=False)
    source_excerpt = Column(Text, nullable=True)
