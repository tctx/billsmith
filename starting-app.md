# Starting BillSmith App

## Development Server

**Port**: `4242` (our crazy port! 🚀)

### Quick Start

1. **Activate virtual environment:**
   ```bash
   source venv/bin/activate
   ```

2. **Start the FastAPI backend:**
   ```bash
   PYTHONPATH=. python -m uvicorn src.backend.main:app --reload --port 4242
   ```

3. **Open in browser:**
   ```
   http://localhost:4242
   ```

### API Endpoints

- **Health Check**: `GET /health`
- **API Documentation**: `GET /docs` (Swagger UI)
- **Categories**: `GET /api/v1/categories`
- **Bills**: `GET /api/v1/bills`
- **Analytics**: `GET /api/v1/analytics/dashboard/{category_id}`

### Development Notes

- Frontend is served from `src/frontend/` at the root `/` path
- API endpoints are available under `/api/v1/`
- Database: SQLite (`billsmith.db` created automatically)
- Default categories are seeded on first startup

### Troubleshooting

- If port 4242 is busy, the app will show "Address already in use"
- Check running processes with: `lsof -i :4242`
- Kill process if needed: `kill -9 <PID>`

### MVP Features Working

✅ Categories API (CRUD)  
✅ Bills API (CRUD + mock creation)  
✅ Analytics API (dashboard data)  
✅ Frontend dashboard with D3 charts  
✅ Responsive design with design tokens  
✅ SQLite database with auto-seeding  

### Next Steps

- [ ] File upload processing
- [ ] OCR + LLM integration
- [ ] Authentication system
- [ ] Real bill extraction pipeline 