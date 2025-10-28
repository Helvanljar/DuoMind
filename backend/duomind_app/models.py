
import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    ForeignKey,
    Boolean,
    Float,
    LargeBinary,
    TIMESTAMP,
    func,
)
from sqlalchemy.orm import relationship

from duomind_app.db import Base


def uuid4_str() -> str:
    return str(uuid.uuid4())


class Session(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, default=uuid4_str)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    user_query = Column(Text, nullable=False)
    status = Column(String, default="draft")
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    notes = relationship(
        "Note", back_populates="session", cascade="all, delete-orphan"
    )
    reports = relationship(
        "Report", back_populates="session", cascade="all, delete-orphan"
    )


class Note(Base):
    __tablename__ = "notes"

    id = Column(String, primary_key=True, default=uuid4_str)
    session_id = Column(
        String, ForeignKey("sessions.id", ondelete="CASCADE"), index=True, nullable=False
    )
    claim = Column(Text, nullable=False)
    evidence_json = Column(Text, nullable=True)
    confidence = Column(Float, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    session = relationship("Session", back_populates="notes")


class Report(Base):
    __tablename__ = "reports"

    id = Column(String, primary_key=True, default=uuid4_str)
    session_id = Column(
        String, ForeignKey("sessions.id", ondelete="CASCADE"), index=True, nullable=False
    )
    markdown = Column(Text, nullable=False)
    verified = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    session = relationship("Session", back_populates="reports")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    credentials = relationship("ApiCredential", backref="user", cascade="all, delete")
    history = relationship("UserQueryHistory", backref="user", cascade="all, delete")
    settings = relationship("UserSettings", backref="user", uselist=False, cascade="all, delete")
    sessions = relationship("Session", backref="user", cascade="all, delete")


class ApiCredential(Base):
    __tablename__ = "api_credentials"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    provider = Column(String, nullable=False)
    key_encrypted = Column(LargeBinary, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    last_used_at = Column(DateTime)


class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, index=True)
    openai_key = Column(String, nullable=True)
    gemini_key = Column(String, nullable=True)
    preferred_llm = Column(String, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class UserQueryHistory(Base):
    __tablename__ = "user_query_history"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    query = Column(Text, nullable=False)
    model_used = Column(String, nullable=True)
    response = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
