"""
Categories API Router

CRUD operations for bill categories.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from ..database import get_session
from ..models import Category, CategoryRead, CategoryCreate, CategoryUpdate

router = APIRouter()


@router.get("/categories", response_model=List[CategoryRead])
async def list_categories(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True,
    session: Session = Depends(get_session)
):
    """List all categories"""
    query = select(Category)
    if active_only:
        query = query.where(Category.active == True)
    
    query = query.offset(skip).limit(limit)
    categories = session.exec(query).all()
    return categories


@router.get("/categories/{category_id}", response_model=CategoryRead)
async def get_category(
    category_id: int,
    session: Session = Depends(get_session)
):
    """Get a specific category"""
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return category


@router.post("/categories", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(
    category: CategoryCreate,
    session: Session = Depends(get_session)
):
    """Create a new category"""
    # Check for duplicate name
    existing = session.exec(
        select(Category).where(Category.name == category.name, Category.active == True)
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name already exists"
        )
    
    db_category = Category(**category.model_dump())
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


@router.patch("/categories/{category_id}", response_model=CategoryRead)
async def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    session: Session = Depends(get_session)
):
    """Update a category"""
    db_category = session.get(Category, category_id)
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    # Check for duplicate name if name is being updated
    if category_update.name and category_update.name != db_category.name:
        existing = session.exec(
            select(Category).where(
                Category.name == category_update.name,
                Category.active == True,
                Category.id != category_id
            )
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category with this name already exists"
            )
    
    # Update fields
    update_data = category_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_category, field, value)
    
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


@router.delete("/categories/{category_id}")
async def archive_category(
    category_id: int,
    session: Session = Depends(get_session)
):
    """Archive a category (soft delete)"""
    db_category = session.get(Category, category_id)
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    # Soft delete by setting active=False
    db_category.active = False
    session.add(db_category)
    session.commit()
    
    return {"message": "Category archived successfully"} 