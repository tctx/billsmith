"""
Bills API Router

CRUD operations for bills and file upload handling.
"""

import os
import uuid
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlmodel import Session, select, desc
from ..database import get_session, get_or_create_category
from ..models import Bill, BillRead, BillCreate, BillUpdate, Category

router = APIRouter()

# File storage configuration
BILLS_STORAGE_PATH = os.getenv("BILLS_STORAGE_PATH", "./Bills")
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", 50))
ALLOWED_FILE_TYPES = os.getenv("ALLOWED_FILE_TYPES", "pdf,png,jpg,jpeg").split(",")


@router.post("/bills/upload")
async def upload_bills(
    files: List[UploadFile] = File(...),
    session: Session = Depends(get_session)
):
    """Upload bill files for processing"""
    job_ids = []
    
    for file in files:
        # Validate file type
        file_ext = file.filename.split(".")[-1].lower() if file.filename else ""
        if file_ext not in ALLOWED_FILE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type {file_ext} not allowed. Allowed types: {ALLOWED_FILE_TYPES}"
            )
        
        # Check file size
        content = await file.read()
        if len(content) > MAX_FILE_SIZE_MB * 1024 * 1024:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File too large. Maximum size: {MAX_FILE_SIZE_MB}MB"
            )
        
        # Generate unique filename and store
        job_id = str(uuid.uuid4())
        temp_path = f"{BILLS_STORAGE_PATH}/temp/{job_id}.{file_ext}"
        
        os.makedirs(os.path.dirname(temp_path), exist_ok=True)
        with open(temp_path, "wb") as f:
            f.write(content)
        
        job_ids.append(job_id)
        # TODO: Queue for processing with Celery
    
    return {"jobs": job_ids, "status": "uploaded", "message": f"Uploaded {len(files)} files"}


@router.get("/bills", response_model=List[BillRead])
async def list_bills(
    skip: int = 0,
    limit: int = 20,
    category_id: Optional[int] = None,
    needs_review: Optional[bool] = None,
    search: Optional[str] = None,
    session: Session = Depends(get_session)
):
    """List bills with filtering and pagination"""
    query = select(Bill).join(Category)
    
    # Filters
    if category_id:
        query = query.where(Bill.category_id == category_id)
    if needs_review is not None:
        query = query.where(Bill.needs_review == needs_review)
    if search:
        search_term = f"%{search}%"
        query = query.where(
            Bill.vendor.contains(search_term) |
            Bill.invoice_number.contains(search_term) |
            Bill.account_number.contains(search_term)
        )
    
    # Order by most recent first
    query = query.order_by(desc(Bill.created_at))
    
    # Pagination
    query = query.offset(skip).limit(limit)
    
    bills = session.exec(query).all()
    return bills


@router.get("/bills/{bill_id}", response_model=BillRead)
async def get_bill(
    bill_id: int,
    session: Session = Depends(get_session)
):
    """Get a specific bill"""
    bill = session.get(Bill, bill_id)
    if not bill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bill not found"
        )
    return bill


@router.patch("/bills/{bill_id}", response_model=BillRead)
async def update_bill(
    bill_id: int,
    bill_update: BillUpdate,
    session: Session = Depends(get_session)
):
    """Update a bill (manual corrections)"""
    db_bill = session.get(Bill, bill_id)
    if not db_bill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bill not found"
        )
    
    # Update fields
    update_data = bill_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_bill, field, value)
    
    # Update timestamp
    db_bill.updated_at = datetime.utcnow()
    
    session.add(db_bill)
    session.commit()
    session.refresh(db_bill)
    return db_bill


@router.delete("/bills/{bill_id}")
async def delete_bill(
    bill_id: int,
    session: Session = Depends(get_session)
):
    """Delete a bill"""
    db_bill = session.get(Bill, bill_id)
    if not db_bill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bill not found"
        )
    
    # Delete file if it exists
    if os.path.exists(db_bill.file_path):
        os.remove(db_bill.file_path)
    
    session.delete(db_bill)
    session.commit()
    
    return {"message": "Bill deleted successfully"}


@router.get("/bills/{bill_id}/file")
async def download_bill_file(
    bill_id: int,
    session: Session = Depends(get_session)
):
    """Download the original bill file"""
    bill = session.get(Bill, bill_id)
    if not bill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bill not found"
        )
    
    if not os.path.exists(bill.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found on disk"
        )
    
    return FileResponse(
        bill.file_path,
        filename=f"{bill.vendor}_{bill.invoice_number or 'invoice'}.{bill.file_path.split('.')[-1]}"
    )


# Temporary endpoint to create a mock bill for testing
@router.post("/bills/mock", response_model=BillRead)
async def create_mock_bill(
    vendor: str = "Test Utility Company",
    amount: float = 125.50,
    category_name: str = "Electricity",
    session: Session = Depends(get_session)
):
    """Create a mock bill for testing (remove in production)"""
    category = get_or_create_category(session, category_name)
    
    mock_bill = Bill(
        category_id=category.id,
        vendor=vendor,
        invoice_number=f"INV-{uuid.uuid4().hex[:8].upper()}",
        account_number=f"ACC-{uuid.uuid4().hex[:10].upper()}",
        amount_due=amount,
        file_path=f"{BILLS_STORAGE_PATH}/mock/mock_bill.pdf",
        needs_review=False,
        confidence_score=0.95
    )
    
    session.add(mock_bill)
    session.commit()
    session.refresh(mock_bill)
    return mock_bill 