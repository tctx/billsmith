"""
BillSmith Database Models

SQLModel entities for categories and bills with all required fields per PRD.
"""

from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, Index


class Category(SQLModel, table=True):
    """Category model for organizing bills"""
    __tablename__ = "categories"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True, max_length=100)
    color_hex: str = Field(default="#2222FF", max_length=7)  # Default blue
    active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    bills: List["Bill"] = Relationship(back_populates="category")


class Bill(SQLModel, table=True):
    """Bill model with extracted data from documents"""
    __tablename__ = "bills"
    
    # Primary fields
    id: Optional[int] = Field(default=None, primary_key=True)
    category_id: int = Field(foreign_key="categories.id", index=True)
    
    # Vendor & Account Info
    vendor: str = Field(max_length=200)
    invoice_number: Optional[str] = Field(default=None, max_length=100)
    account_number: Optional[str] = Field(default=None, max_length=100)
    
    # Billing Period
    billing_start: Optional[date] = Field(default=None)
    billing_end: Optional[date] = Field(default=None)
    due_date: Optional[date] = Field(default=None, index=True)
    
    # Financial Data
    amount_due: Decimal = Field(max_digits=10, decimal_places=2)
    usage_qty: Optional[Decimal] = Field(default=None, max_digits=10, decimal_places=3)
    usage_unit: Optional[str] = Field(default=None, max_length=50)
    tax_total: Optional[Decimal] = Field(default=None, max_digits=10, decimal_places=2)
    
    # File & Processing
    file_path: str = Field(max_length=500)
    needs_review: bool = Field(default=False, index=True)
    confidence_score: Optional[float] = Field(default=None)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    category: Category = Relationship(back_populates="bills")
    
    # Database indexes for performance
    __table_args__ = (
        Index("idx_category_due_date", "category_id", "due_date"),
        Index("idx_vendor", "vendor"),
        Index("idx_created_at", "created_at"),
    )


# Pydantic models for API responses
class CategoryRead(SQLModel):
    """Category response model"""
    id: int
    name: str
    color_hex: str
    active: bool
    created_at: datetime


class CategoryCreate(SQLModel):
    """Category creation model"""
    name: str
    color_hex: str = "#2222FF"


class CategoryUpdate(SQLModel):
    """Category update model"""
    name: Optional[str] = None
    color_hex: Optional[str] = None
    active: Optional[bool] = None


class BillRead(SQLModel):
    """Bill response model"""
    id: int
    category_id: int
    vendor: str
    invoice_number: Optional[str]
    account_number: Optional[str]
    billing_start: Optional[date]
    billing_end: Optional[date]
    due_date: Optional[date]
    amount_due: Decimal
    usage_qty: Optional[Decimal]
    usage_unit: Optional[str]
    tax_total: Optional[Decimal]
    file_path: str
    needs_review: bool
    confidence_score: Optional[float]
    created_at: datetime
    updated_at: datetime
    category: CategoryRead


class BillCreate(SQLModel):
    """Bill creation model"""
    category_id: int
    vendor: str
    invoice_number: Optional[str] = None
    account_number: Optional[str] = None
    billing_start: Optional[date] = None
    billing_end: Optional[date] = None
    due_date: Optional[date] = None
    amount_due: Decimal
    usage_qty: Optional[Decimal] = None
    usage_unit: Optional[str] = None
    tax_total: Optional[Decimal] = None
    file_path: str
    needs_review: bool = False
    confidence_score: Optional[float] = None


class BillUpdate(SQLModel):
    """Bill update model for manual corrections"""
    category_id: Optional[int] = None
    vendor: Optional[str] = None
    invoice_number: Optional[str] = None
    account_number: Optional[str] = None
    billing_start: Optional[date] = None
    billing_end: Optional[date] = None
    due_date: Optional[date] = None
    amount_due: Optional[Decimal] = None
    usage_qty: Optional[Decimal] = None
    usage_unit: Optional[str] = None
    tax_total: Optional[Decimal] = None
    needs_review: Optional[bool] = None 