# Product Requirements Document

**Project**: BillSmith – Automated Personal Bill Manager  
**Date**: 30 May 2025  
**Authoring Model**: OpenAI o3 (leveraging gpt-4o for document understanding)

## 1. Vision & Goals

### Vision
Create a system where a user can drop any bill (PDF, image, e-mail) into the app and instantly receive a clean, searchable record, insightful analytics, and an archived copy—all with zero manual data entry.

### Primary Goals for MVP
- Accept manual uploads for the three launch categories: Electricity, Water, Gas.
- Achieve ≥ 99% field-level accuracy using a hybrid OCR + LLM pipeline (gpt-4o).
- Persist records in a local SQL database and store source files under a deterministic folder path.
- Render a dashboard UI identical in spirit to the reference screenshot (minimalist, dark-on-white).
- Provide full CRUD for bill categories (add, rename, archive).

### Secondary (Architectural) Goals
- Stripe-powered paywall (flag-gated and disabled by default).
- Gmail / "forward-to-inbox" ingestion hooks.
- Future negotiating agent that proactively lowers bills.
- Month-over-month / year-over-year comparison page.

## 2. Scope of This PRD

This document contains all functional, non-functional, and technical specifications for the MVP plus hooks for future features.

- Python backend, vanilla JavaScript frontend, D3.js for data visualization.
- No Tailwind; only handcrafted CSS with system fonts.
- Written for an autonomous agentic AI coder—all instructions are explicit and deterministic.

## 3. Detailed Functional Requirements

### F-01: Upload
- User drags, drops, or selects one or more bill files.
- Supported file types: PDF, PNG, JPG.
- Front-end shows a skeleton "processing" card per file.
- Backend immediately returns `{"recordId", "status":"processing"}` with HTTP 200.

### F-02: Extraction
System must extract and normalize these fields, regardless of layout:
- Vendor name
- Account number
- Invoice number
- Billing period (start & end)
- Due date
- Total amount due
- Usage quantity & unit
- Tax line items
- Address block
- Contact phone / URL

**Requirements**:
- Numeric and date fields must hit ≥ 99% accuracy.
- If confidence < 0.9, mark the record needs-review (yellow badge in UI).

### F-03: Storage
- Source file moved to: `/Bills/{Category}/{YYYY}/{Vendor}/{Invoice#}.pdf`
- Directory tree auto-creates as needed.
- Database row stores the absolute file path.

### F-04: Categorization
System uses a two-step approach:
1. Vendor-alias lookup table.
2. gpt-4o zero-shot classification fallback.
3. User can manually override category.

### F-05: Dashboard
Landing page shows:
- Left rail with category list.
- Hero card for selected category.
- D3 line chart displaying payment trends.
- Three summary cards (Last Payment, Next Due, Year-to-Date).
- List of important documents.

### F-06: Search & Filter
- Global search bar filters by any field.
- ≤ 150 ms search latency with 300 ms debounce.

### F-07: Create Category
- "+ New Category" modal with name and color picker (hex).
- Must enforce unique names.

### F-08: Edit / Delete Category
- Rename updates every associated record.
- Delete simply flags the category inactive; bills remain visible via "All Bills".

### F-09: Insights
Each category view also shows:
- Total spent YTD
- Highest monthly spend
- Average spend
- Next due date

### F-10: Permissions & Auth
- Single-user local password (bcrypt) and JWT.
- Multi-tenant reserved for future.

### F-11: Paywall
- If environment variable `ENABLE_PAYWALL=true`, unauthenticated requests redirect to `/pay`.
- Uses pre-built Stripe Checkout link placeholder.

### F-12: API-First
- All UI functionality backed by versioned REST endpoints under `/api/v1`.
- Auto-generated OpenAPI/Swagger spec.

## 4. Non-Functional Requirements

### Performance
- Page load (P95) under 300 ms on localhost.
- Extraction queue ≤ 10 s per file.

### Scalability
- Docker Compose stack.
- Toggle SQLite → Postgres via env var.

### Security
- Files stored as non-executable.
- Directory traversal protections.
- JWT expiry set to 1 hour.

### Reliability
- Automatic retries (3×) on OCR or GPT failures with exponential backoff.

### Accessibility
- WCAG 2.1 AA color contrast.
- Full keyboard navigation.

### Responsive Design
- Breakpoints at < 600 px (mobile), 600-1024 px (tablet), > 1024 px (desktop).

## 5. System Architecture

**Frontend SPA** (vanilla ES2022 modules) communicates over REST and WebSockets.

**FastAPI Core** provides endpoints, JWT auth, and serves the single-page app.

**Celery Worker Pool** processes extraction jobs asynchronously, using Redis as broker.

**Database & File Store**: Local SQLite (default) with file paths pointing to the deterministic folder tree.

**Future Micro-services** (negotiation agent, Gmail ingest) connect via Redis queue.

## 6. Extraction Pipeline (Hybrid OCR + gpt-4o)

1. **Queue Job** – Create Job(id, filepath, status="queued").
2. **Pre-Parse PDF** – If PDF, use pdfplumber; if image, convert to PNG via Pillow.
3. **OCR Fallback** – Run Tesseract 5 on pages with < 100 characters extracted.
4. **Heuristic Field Grab** – Regex for money and date patterns to seed a context dict.
5. **gpt-4o Call 1 (Field Completion)** –
   - system: "You are an expert bill parser…"
   - user: JSON schema + raw text snippets (< 32k).
   - Model responds with fully-populated JSON.
6. **gpt-4o Call 2 (Confidence Scoring)** – Ask the model for per-field confidence 0–1.
7. **Post-Process** – Normalize dates (ISO-8601) and currency (¢ precision).
8. **Persist** – Write BillRecord row and move file to permanent location.
9. **Notify Front-End** – WebSocket update: status done or needs-review.

## 7. Data Model (SQLModel)

### Category Entity
**Fields**: 
- id
- name
- color_hex (default #2222FF)
- active (bool)

### Bill Entity
**Fields**:
- id
- category_id (FK → Category)
- vendor
- invoice_number
- account_number
- billing_start (date)
- billing_end (date)
- due_date (date)
- amount_due (decimal, 10,2)
- usage_qty (optional decimal)
- usage_unit (optional string)
- tax_total (optional decimal)
- file_path (string)
- created_at (datetime)
- needs_review (bool)

**Secondary Indices**:
- Composite (category_id, due_date)
- Single column vendor

## 8. API Contract (Excerpt)

### POST /api/v1/bills/upload
- **Body**: multipart/form-data with files[].
- **Returns**: 202 Accepted `{ "jobs": [<id>, …] }`.

### GET /api/v1/bills/{id}
- **Returns**: 200 Bill JSON.

### PATCH /api/v1/bills/{id}
- **Body**: partial JSON for manual corrections.
- **Returns**: updated Bill JSON.

### GET /api/v1/categories
- List all categories.

### POST /api/v1/categories
- Create category with `{name, color_hex}`.

*(Swagger/OpenAPI auto-generated for full coverage.)*

## 9. Front-End Page Inventory & Design Specs

### P-00: Login (/login)
- Centered card, app logo, email + password inputs.
- Primary button: gradient #111111 → #444444 (lightens on hover).

### P-01: Dashboard Home (/)
- **Sticky header**: logo (left), "Add Bill" (right).
- **Left rail**: vertical category list, scrollable when > 6 items.
- **Main panel**:
  - Bill Pay Dashboard heading.
  - Hero category card mimicking reference design.
  - D3 line chart for payment trends.
  - Three summary cards.
  - Important documents list (each row: icon, filename, date, view/download buttons).

### P-02: Bill Detail (/bill/:id)
- Back arrow in top bar.
- **Two-column layout**:
  - Left: editable form of extracted fields.
  - Right: embedded PDF viewer.
- "Edit metadata" toggle enters editable mode.

### P-03: Category Modal (#modal-category)
- Form fields: name, color picker.
- Save and Cancel buttons.

### P-04: Search Results (/search?q=)
- Table of results (vendor, amount, due, category badge).
- Click row → Bill Detail.

### P-05: Paywall (/pay)
- Marketing copy outlining value props.
- Pricing card with Stripe Checkout button.

### P-06: Settings (/settings)
**Accordion sections**:
- Profile
- Storage path (browse button)
- LLM API key field
- Beta feature toggles

### P-07: Insights (Future) (/insights)
- Placeholder matrix of sparklines per category.
- MoM table reserved for future release.

### P-08: 404 (/404)
- Whimsical illustration + link to dashboard.

### Shared Layout Tokens
- **Font stack**: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto.
- **Text colors**: primary #222, secondary #666, accent = category color.
- **Card**: 8 px radius, 0 1 3 px rgba(0,0,0,0.08) shadow.

### Mobile Adjustments
- Category rail collapses into a top dropdown.
- Chart becomes 100% width; document list stacks.

## 10. CSS Strategy

- Single styles.css using BEM naming.
- **Core classes**: .card, .btn-primary, .chart-container, .sidebar.
- Layout via CSS Grid + Flexbox.
- Media queries at 600 px and 1024 px.
- Only ~200 lines of custom CSS; no third-party framework.

## 11. Pseudocode Snippets

### FastAPI Endpoint
```python
# FastAPI endpoint
@router.post("/bills/upload", status_code=202)
async def upload(files: list[UploadFile]):
    job_ids = []
    for f in files:
        tmp_path = save_temp(f)
        jid = celery_app.send_task("tasks.extract", args=[tmp_path])
        job_ids.append(jid)
    return {"jobs": job_ids}
```

### Front-end File Drop
```javascript
// front-end file drop
dropZone.on('change', async (evt) => {
  const files = [...evt.target.files];
  const form = new FormData();
  files.forEach(f => form.append("files[]", f));
  const res = await fetch("/api/v1/bills/upload", {method:"POST", body:form});
  const {jobs} = await res.json();
  jobs.forEach(renderProcessingCard);
});
```

## 12. Future-Proofing Hooks

### Gmail Ingest
- Celery worker already isolated; add an IMAP listener task driven by IMAP_URI.

### Negotiation Agent
- Separate micro-service writing suggestions to an Advise table; UI displays tips.

### Multi-Tenant SaaS
- Prepared DB migrations; set MULTI_TENANT=true to enable.

### Stripe Paywall
- /pay route and middleware exist; flip environment flag and insert live keys.

## 13. Security & Privacy Notes

- All GPT-4o calls via HTTPS; mask PII (e.g., replace street address with `<ADDR>` token) before sending.
- Stored PDFs inherit OS-level permissions; the app process runs under a least-privilege user.
- Optional setting to auto-delete raw files after a configurable number of days.

## 14. Glossary

- **LLM** – Large Language Model (gpt-4o).
- **Heuristic Grab** – Regex + lookup pre-fill step before GPT.
- **Needs Review** – Bill flagged for manual user validation.
- **Category Rail** – Vertical navigation area on the left side of the dashboard.

## 15. Delivery Milestones

1. **Week 1** – Repo bootstrap, DB schema, authentication scaffold.
2. **Week 2** – File upload/store logic; Celery job skeleton.
3. **Week 3** – OCR pipeline + GPT-4o extraction with dev keys.
4. **Week 4** – Category dashboard UI (desktop).
5. **Week 5** – Responsive tweaks, global search, insights calculations.
6. **Week 6** – Polish, docs, Dockerfile, smoke tests.

## 16. Ready-for-Agent Checklist

- ✓ Explicit REST endpoints and JSON schemas present.
- ✓ Database schema fully described.
- ✓ CSS tokens and breakpoints documented.
- ✓ LLM prompt template + confidence handshake defined.
- ✓ Docker Compose outline and required environment variables noted.
- ✓ Future feature stubs annotated.

