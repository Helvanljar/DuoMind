from __future__ import annotations

from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Always resolve DB path relative to this package folder (NOT the current working directory).
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "duomind.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

DATABASE_URL = f"sqlite:///{DB_PATH.as_posix()}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    future=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
Base = declarative_base()


def init_db() -> None:
    """Create tables if they don't exist (safe to call multiple times)."""
    # Import models here to avoid circular imports.
    from . import models  # noqa: F401
    Base.metadata.create_all(bind=engine)
