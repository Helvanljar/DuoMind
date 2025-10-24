
import uuid
from sqlalchemy import Column, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from .db import Base

def uuid4_str():
    return str(uuid.uuid4())

class Session(Base):
    __tablename__ = "sessions"
    id = Column(String, primary_key=True, default=uuid4_str)
    user_query = Column(Text, nullable=False)
    status = Column(String, default="draft")  # draft|complete (erweitern wir später)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
