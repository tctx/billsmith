"""
BillSmith FastAPI Application

Main application with routing, middleware, and configuration.
"""

import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager

from .database import create_db_and_tables, init_default_categories
from .routers import categories, bills, analytics


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print("🚀 Starting BillSmith...")
    create_db_and_tables()
    init_default_categories()
    print("✅ Database initialized")
    yield
    # Shutdown
    print("👋 Shutting down BillSmith...")


# Create FastAPI app
app = FastAPI(
    title="BillSmith API",
    description="Automated Personal Bill Manager with AI extraction",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
origins = os.getenv("CORS_ORIGINS", "http://localhost:4242,http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routers
app.include_router(categories.router, prefix="/api/v1", tags=["categories"])
app.include_router(bills.router, prefix="/api/v1", tags=["bills"])
app.include_router(analytics.router, prefix="/api/v1", tags=["analytics"])

# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "app": "BillSmith", "port": "4242"}

# Serve frontend static files
if os.path.exists("src/frontend"):
    app.mount("/static", StaticFiles(directory="src/frontend"), name="static")

# Serve the main index.html for SPA
@app.get("/")
async def serve_frontend():
    """Serve the main frontend application"""
    frontend_path = "src/frontend/index.html"
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    else:
        return {"message": "BillSmith API is running on port 4242. Frontend not yet built."}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 4242))
    host = os.getenv("HOST", "0.0.0.0")
    
    uvicorn.run(
        "src.backend.main:app",
        host=host,
        port=port,
        reload=bool(os.getenv("RELOAD", True))
    ) 