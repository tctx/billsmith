# BillSmith – Automated Personal Bill Manager

**One inbox for every bill.**

BillSmith is an intelligent bill management system that automatically extracts, categorizes, and organizes your utility bills with zero manual data entry. Drop any bill (PDF, image, email) and instantly receive a clean, searchable record with insightful analytics.

## 🚀 Vision

Create a system where users can drop any bill into the app and instantly receive:
- ✅ Clean, searchable records
- 📊 Insightful analytics  
- 📁 Automatically archived copies
- 🎯 Zero manual data entry

## ✨ Features

### MVP Core Features
- **Smart Upload**: Drag & drop PDFs, PNGs, JPGs with instant processing
- **AI Extraction**: 99%+ field accuracy using hybrid OCR + GPT-4o pipeline
- **Auto-Categorization**: Intelligent vendor recognition and bill categorization
- **Interactive Dashboard**: D3.js visualizations with payment trends and insights
- **Advanced Search**: Global search with ≤150ms latency and smart filtering
- **Category Management**: Full CRUD operations with color-coded organization

### Supported Bill Types (Launch)
- ⚡ **Electricity** bills
- 💧 **Water** utilities  
- 🔥 **Gas** services

### Future Features
- 📧 Gmail integration with forward-to-inbox
- 🤝 Bill negotiation agent
- 💳 Stripe-powered premium features
- 📈 Month-over-month comparisons

## 🛠 Tech Stack

### Backend
- **FastAPI** - High-performance Python web framework
- **SQLModel** - Type-safe database interactions
- **Celery + Redis** - Asynchronous task processing
- **Tesseract 5** - OCR text extraction
- **pdfplumber** - PDF parsing
- **OpenAI GPT-4o** - Intelligent field extraction

### Frontend
- **Vanilla JavaScript ES2022** - No framework dependencies
- **D3.js** - Data visualization and charts
- **CSS Grid + Flexbox** - Responsive layout system
- **BEM methodology** - Maintainable CSS architecture

### Infrastructure
- **Docker Compose** - Local development environment
- **SQLite/PostgreSQL** - Database (configurable)
- **WebSockets** - Real-time processing updates

## 🎨 Design System

### Color Palette
- **Primary**: #222222 (Ink) - headings & body text
- **Secondary**: #666666 (Graphite) - labels & secondary text  
- **Background**: #F8F9FA (Paper) - surface backgrounds
- **Accent**: Dynamic category colors (default #2222FF)

### Typography
- **Font Stack**: `system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto`
- **Responsive scaling**: 1.0 (desktop), 0.95 (tablet), 0.9 (mobile)

### Interactions
- **Button press**: 120ms cubic-bezier(.4,0,.2,1)
- **Modal transitions**: 240ms ease-out
- **Chart animations**: Transform & opacity only (text crispness)

## 📋 Project Structure

```
billsmith/
├── instructions/           # 📚 Project documentation
│   ├── prd.md             # Product Requirements Document
│   ├── checklist.md       # Development task tracker
│   ├── style-guide.md     # UI/UX specifications
│   ├── user-journey.md    # User experience flows
│   └── push.md           # Git commit guidelines
├── src/                   # 💻 Application source code
│   ├── backend/          # FastAPI application
│   ├── frontend/         # Vanilla JS + CSS
│   └── shared/           # Common utilities
├── tests/                # 🧪 Test suites
├── docs/                 # 📖 Additional documentation
├── docker-compose.yml    # 🐳 Development environment
├── requirements.txt      # 📦 Python dependencies
└── .env.example         # ⚙️ Environment variables template
```

## 🚦 Getting Started

### Prerequisites
- **Python 3.11+**
- **Docker & Docker Compose**
- **Redis** (for Celery)
- **Tesseract 5** (for OCR)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/billsmith.git
   cd billsmith
   ```

2. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Start development environment**
   ```bash
   docker-compose up -d
   ```

4. **Install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

5. **Initialize database**
   ```bash
   python -m src.backend.init_db
   ```

6. **Start the application**
   ```bash
   # Terminal 1: FastAPI server
   uvicorn src.backend.main:app --reload --port 8000
   
   # Terminal 2: Celery worker
   celery -A src.backend.celery_app worker --loglevel=info
   
   # Terminal 3: Redis (if not using Docker)
   redis-server
   ```

7. **Open your browser**
   Navigate to `http://localhost:8000`

## 📊 Data Extraction Pipeline

BillSmith uses a sophisticated hybrid approach for maximum accuracy:

```mermaid
graph LR
    A[Upload Bill] --> B[Pre-parse PDF/Image]
    B --> C[OCR with Tesseract]
    C --> D[Heuristic Field Grab]
    D --> E[GPT-4o Field Completion]
    E --> F[GPT-4o Confidence Scoring]
    F --> G[Data Validation & Normalization]
    G --> H[Store + Categorize]
    H --> I[WebSocket Notification]
```

### Extracted Fields
- 🏢 **Vendor name**
- 🔢 **Account number**  
- 📄 **Invoice number**
- 📅 **Billing period** (start & end)
- ⏰ **Due date**
- 💰 **Total amount due**
- ⚡ **Usage quantity & unit**
- 🧾 **Tax line items**
- 📍 **Address block**
- 📞 **Contact information**

## 🎯 User Personas

### 1. **"Jessica the Home-Renter"**
- **Goal**: Single source of truth for 6+ utility bills
- **Pain**: Tired of digging through emails
- **Success**: Weekly active use, zero late fees

### 2. **"Raj the Small-Biz Owner"** 
- **Goal**: Track utilities + SaaS for tax season
- **Pain**: Needs exportable, categorized data
- **Success**: CSV exports, category control

### 3. **"Sam the Power User"**
- **Goal**: Upload 10 years of PDFs, evaluate data viz
- **Pain**: Wants comprehensive analytics
- **Success**: Retention after bulk upload, social sharing

## 🔒 Security & Privacy

- **PII Masking**: Address data masked before sending to GPT-4o
- **JWT Authentication**: 1-hour expiry with secure session management
- **File Security**: Non-executable storage with directory traversal protection
- **HTTPS Only**: All API communications encrypted
- **Data Retention**: Optional auto-deletion after configurable days

## 🧪 Testing

### Run Tests
```bash
# Unit tests
pytest tests/unit/

# Integration tests  
pytest tests/integration/

# End-to-end tests
pytest tests/e2e/

# All tests with coverage
pytest --cov=src tests/
```

### Performance Targets
- **Page load**: <300ms (P95)
- **Search latency**: ≤150ms
- **Extraction time**: ≤10s per file
- **File size limit**: 50MB hard limit

## 📈 Development Roadmap

### Phase 1: Foundation ✅
- [x] Project setup & documentation
- [ ] Database models & authentication
- [ ] Core API structure

### Phase 2: Core Pipeline 🚧
- [ ] File upload & storage
- [ ] OCR + LLM integration
- [ ] Data extraction pipeline

### Phase 3: Frontend 📅
- [ ] Design system implementation
- [ ] Dashboard & visualizations
- [ ] Bill management interface

### Phase 4: Polish 📅
- [ ] Testing & optimization
- [ ] Security hardening
- [ ] Documentation completion

## 🤝 Contributing

We follow strict development guidelines to ensure code quality:

### Commit Messages
Follow the format in `instructions/push.md`:
```
add feature description in imperative voice

- Feature Area: specific implementation detail
- Tests: add corresponding test coverage
- Docs: update relevant documentation
```

### Code Standards
- **Python**: Black formatting, type hints, SQLModel
- **JavaScript**: ES2022 modules, functional patterns
- **CSS**: BEM methodology, design tokens, responsive-first

### Pull Request Process
1. Create feature branch from `main`
2. Follow checklist in `instructions/checklist.md`
3. Ensure all tests pass
4. Update documentation
5. Request review

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI GPT-4o** for intelligent text extraction
- **Tesseract** for reliable OCR processing
- **FastAPI** for the excellent async framework
- **D3.js** for powerful data visualizations

---

**Built with ❤️ for simplifying bill management**

*"One inbox for every bill" - BillSmith Team* 