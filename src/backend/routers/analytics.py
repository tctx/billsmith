"""
Analytics API Router

Dashboard insights, spending analytics, and chart data.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, date, timedelta
from decimal import Decimal
from fastapi import APIRouter, Depends
from sqlmodel import Session, select, func, and_, extract
from ..database import get_session
from ..models import Bill, Category

router = APIRouter()


@router.get("/analytics/dashboard/{category_id}")
async def get_category_dashboard(
    category_id: int,
    session: Session = Depends(get_session)
):
    """Get dashboard data for a specific category"""
    
    # Get category info
    category = session.get(Category, category_id)
    if not category:
        return {"error": "Category not found"}
    
    # Get bills for this category
    bills = session.exec(
        select(Bill)
        .where(Bill.category_id == category_id)
        .order_by(Bill.created_at.desc())
    ).all()
    
    if not bills:
        return {
            "category": {
                "id": category.id,
                "name": category.name,
                "color_hex": category.color_hex
            },
            "summary": {
                "last_payment": None,
                "next_due": None,
                "year_to_date": 0
            },
            "payment_trends": [],
            "important_documents": []
        }
    
    # Calculate summary metrics
    current_year = datetime.now().year
    ytd_total = sum(
        bill.amount_due for bill in bills 
        if bill.created_at.year == current_year
    )
    
    # Last payment
    last_payment = {
        "amount": float(bills[0].amount_due),
        "date": bills[0].created_at.date().isoformat(),
        "vendor": bills[0].vendor
    } if bills else None
    
    # Next due date (find earliest due date in future)
    now = date.today()
    upcoming_bills = [b for b in bills if b.due_date and b.due_date >= now]
    next_due = min(upcoming_bills, key=lambda x: x.due_date).due_date.isoformat() if upcoming_bills else None
    
    # Payment trends (last 12 months)
    trends = []
    for i in range(12):
        month_date = datetime.now() - timedelta(days=30 * i)
        month_bills = [
            b for b in bills 
            if b.created_at.month == month_date.month and b.created_at.year == month_date.year
        ]
        month_total = sum(bill.amount_due for bill in month_bills)
        
        trends.append({
            "date": month_date.strftime("%Y-%m"),
            "amount": float(month_total)
        })
    
    trends.reverse()  # Chronological order
    
    # Important documents (last 5)
    documents = []
    for bill in bills[:5]:
        documents.append({
            "id": bill.id,
            "title": f"{bill.vendor} - {bill.invoice_number or 'Invoice'}",
            "date": bill.created_at.date().isoformat(),
            "amount": float(bill.amount_due),
            "needs_review": bill.needs_review
        })
    
    return {
        "category": {
            "id": category.id,
            "name": category.name,
            "color_hex": category.color_hex
        },
        "summary": {
            "last_payment": last_payment,
            "next_due": next_due,
            "year_to_date": float(ytd_total)
        },
        "payment_trends": trends,
        "important_documents": documents
    }


@router.get("/analytics/spending/summary")
async def get_spending_summary(
    year: Optional[int] = None,
    session: Session = Depends(get_session)
):
    """Get overall spending summary by category"""
    
    if not year:
        year = datetime.now().year
    
    # Get spending by category for the year
    query = (
        select(
            Category.id,
            Category.name,
            Category.color_hex,
            func.sum(Bill.amount_due).label("total_spent"),
            func.count(Bill.id).label("bill_count"),
            func.avg(Bill.amount_due).label("avg_amount"),
            func.max(Bill.amount_due).label("max_amount")
        )
        .select_from(Category)
        .join(Bill)
        .where(extract("year", Bill.created_at) == year)
        .group_by(Category.id, Category.name, Category.color_hex)
        .order_by(func.sum(Bill.amount_due).desc())
    )
    
    results = session.exec(query).all()
    
    categories = []
    total_yearly = 0
    
    for result in results:
        category_data = {
            "category_id": result.id,
            "category_name": result.name,
            "color_hex": result.color_hex,
            "total_spent": float(result.total_spent or 0),
            "bill_count": result.bill_count,
            "avg_amount": float(result.avg_amount or 0),
            "max_amount": float(result.max_amount or 0)
        }
        categories.append(category_data)
        total_yearly += category_data["total_spent"]
    
    return {
        "year": year,
        "total_yearly": total_yearly,
        "categories": categories
    }


@router.get("/analytics/trends/monthly")
async def get_monthly_trends(
    months: int = 12,
    category_id: Optional[int] = None,
    session: Session = Depends(get_session)
):
    """Get monthly spending trends"""
    
    trends = []
    
    for i in range(months):
        month_date = datetime.now() - timedelta(days=30 * i)
        month = month_date.month
        year = month_date.year
        
        query = select(func.sum(Bill.amount_due)).where(
            and_(
                extract("month", Bill.created_at) == month,
                extract("year", Bill.created_at) == year
            )
        )
        
        if category_id:
            query = query.where(Bill.category_id == category_id)
        
        result = session.exec(query).first()
        amount = float(result or 0)
        
        trends.append({
            "month": month_date.strftime("%Y-%m"),
            "amount": amount
        })
    
    trends.reverse()  # Chronological order
    return {"trends": trends}


@router.get("/analytics/categories/performance")
async def get_category_performance(
    session: Session = Depends(get_session)
):
    """Get performance metrics for all categories"""
    
    categories = session.exec(select(Category).where(Category.active == True)).all()
    performance = []
    
    for category in categories:
        bills = session.exec(
            select(Bill).where(Bill.category_id == category.id)
        ).all()
        
        if not bills:
            continue
        
        total_spent = sum(bill.amount_due for bill in bills)
        avg_amount = total_spent / len(bills) if bills else 0
        
        # Get last 3 months trend
        three_months_ago = datetime.now() - timedelta(days=90)
        recent_bills = [b for b in bills if b.created_at >= three_months_ago]
        recent_total = sum(bill.amount_due for bill in recent_bills)
        
        performance.append({
            "category_id": category.id,
            "category_name": category.name,
            "color_hex": category.color_hex,
            "total_bills": len(bills),
            "total_spent": float(total_spent),
            "avg_amount": float(avg_amount),
            "recent_3m_total": float(recent_total),
            "needs_review_count": len([b for b in bills if b.needs_review])
        })
    
    # Sort by total spent descending
    performance.sort(key=lambda x: x["total_spent"], reverse=True)
    
    return {"categories": performance} 