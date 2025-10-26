
import uuid
from sqlalchemy import Column, String, Text, TIMESTAMP, Float, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .db import Base

def uuid4_str():
    return str(uuid.uuid4())

class Session(Base):
    __tablename__ = "sessions"
    id = Column(String, primary_key=True, default=uuid4_str)
    user_query = Column(Text, nullable=False)
    status = Column(String, default="draft")  # draft|complete
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    notes = relationship("Note", back_populates="session", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="session", cascade="all, delete-orphan")

class Note(Base):
    __tablename__ = "notes"
    id = Column(String, primary_key=True, default=uuid4_str)
    session_id = Column(String, ForeignKey("sessions.id", ondelete="CASCADE"), index=True, nullable=False)
    claim = Column(Text, nullable=False)
    evidence_json = Column(Text, nullable=True)
    confidence = Column(Float, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    session = relationship("Session", back_populates="notes")

class Report(Base):
    __tablename__ = "reports"
    id = Column(String, primary_key=True, default=uuid4_str)
    session_id = Column(String, ForeignKey("sessions.id", ondelete="CASCADE"), index=True, nullable=False)
    markdown = Column(Text, nullable=False)
    verified = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    session = relationship("Session", back_populates="reports")
