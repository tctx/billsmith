"""
Database configuration and connection management
"""

import os
from sqlmodel import SQLModel, create_engine, Session, select
from typing import Generator
from .models import Category, Bill

# Database URL from environment or default to SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./billsmith.db")

# Create engine with appropriate settings
if DATABASE_URL.startswith("sqlite"):
    # SQLite configuration
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=bool(os.getenv("DEBUG_MODE", False))
    )
else:
    # PostgreSQL configuration
    engine = create_engine(DATABASE_URL, echo=bool(os.getenv("DEBUG_MODE", False)))


def create_db_and_tables():
    """Create database tables"""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Dependency for getting database session"""
    with Session(engine) as session:
        yield session


def init_default_categories():
    """Initialize default categories for the MVP"""
    with Session(engine) as session:
        # Check if categories already exist
        existing = session.exec(select(Category)).first()
        if existing:
            return
        
        # Create default categories per PRD
        default_categories = [
            Category(name="Electricity", color_hex="#FFB800"),  # Orange
            Category(name="Water", color_hex="#00B4FF"),        # Blue 
            Category(name="Gas", color_hex="#FF6B00"),          # Red-Orange
            Category(name="Rent", color_hex="#2222FF"),         # Default blue
            Category(name="Internet", color_hex="#9C27B0"),     # Purple
            Category(name="Phone", color_hex="#4CAF50"),        # Green
        ]
        
        for category in default_categories:
            session.add(category)
        
        session.commit()
        print(f"✅ Created {len(default_categories)} default categories")


def get_category_by_name(session: Session, name: str) -> Category | None:
    """Get category by name"""
    return session.exec(select(Category).where(Category.name == name, Category.active == True)).first()


def get_or_create_category(session: Session, name: str, color_hex: str = "#2222FF") -> Category:
    """Get existing category or create new one"""
    category = get_category_by_name(session, name)
    if not category:
        category = Category(name=name, color_hex=color_hex)
        session.add(category)
        session.commit()
        session.refresh(category)
    return category 