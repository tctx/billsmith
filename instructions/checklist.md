# BillSmith Development Checklist

## Instructions for AI

**This is a living, breathing checklist for building the BillSmith app.** 

### Usage Rules:
- ✅ Mark items as **Done** when completed
- ➕ **ADD** new tasks as they become apparent during development
- ✏️ **EDIT** tasks to be more specific or accurate as needed
- 🗑️ **DELETE** tasks that become irrelevant
- 🤔 **After marking any item as Done**: Think through what else might need to be added to the checklist
- 🎯 **Suggest Next**: Always suggest the most logical next task to tackle

### Status Legend:
- ⏳ **Pending** - Not started
- 🚧 **In Progress** - Currently working on
- ✅ **Done** - Completed
- ❌ **Blocked** - Cannot proceed (note reason)
- 🔄 **Needs Review** - Completed but needs validation

---

## Phase 1: Project Foundation & Setup

### Repository & Environment
- ⏳ Initialize Git repository with proper `.gitignore`
- ⏳ Create project directory structure
- ⏳ Set up virtual environment (Python)
- ⏳ Create `requirements.txt` with initial dependencies
- ⏳ Create `.env` file with API keys (already provided)
- ⏳ Set up Docker Compose configuration
- ⏳ Create basic `README.md` with setup instructions

### Database Schema & Models
- ⏳ Install SQLModel and database dependencies
- ⏳ Create `Category` model with fields: id, name, color_hex, active
- ⏳ Create `Bill` model with all required fields per PRD
- ⏳ Set up database connection and configuration
- ⏳ Create database migrations/initialization script
- ⏳ Add secondary indices: (category_id, due_date), vendor
- ⏳ Test database models with sample data

### Authentication & Security Foundation
- ⏳ Install FastAPI security dependencies (JWT, bcrypt)
- ⏳ Create user authentication models
- ⏳ Implement password hashing with bcrypt
- ⏳ Create JWT token generation and validation
- ⏳ Set up login/logout endpoints
- ⏳ Add authentication middleware
- ⏳ Implement 1-hour JWT expiry

---

## Phase 2: Core Backend Infrastructure

### FastAPI Application Setup
- ⏳ Create FastAPI application instance
- ⏳ Set up CORS configuration
- ⏳ Create router structure for `/api/v1/`
- ⏳ Add request/response logging middleware
- ⏳ Set up error handling and validation
- ⏳ Create health check endpoint
- ⏳ Generate OpenAPI/Swagger documentation

### File Upload & Storage System
- ⏳ Create file upload endpoint `POST /api/v1/bills/upload`
- ⏳ Implement multipart/form-data handling
- ⏳ Add file type validation (PDF, PNG, JPG)
- ⏳ Create deterministic folder structure `/Bills/{Category}/{YYYY}/{Vendor}/{Invoice#}.pdf`
- ⏳ Implement secure file storage with proper permissions
- ⏳ Add directory traversal protection
- ⏳ Return immediate response with job IDs
- ⏳ Implement 50 MB hard limit for file uploads
- ⏳ Add per-file progress tracking for large uploads

### Celery Task Queue Setup
- ⏳ Install and configure Celery with Redis broker
- ⏳ Create Celery worker configuration
- ⏳ Set up task queue for file processing
- ⏳ Implement job status tracking
- ⏳ Add retry logic with exponential backoff (3x retries)
- ⏳ Create WebSocket notifications for job completion
- ⏳ Add fallback SMS/email notification for long OCR waits (>30s)

---

## Phase 3: OCR & LLM Processing Pipeline

### OCR Implementation
- ⏳ Install Tesseract 5 and dependencies
- ⏳ Install pdfplumber for PDF text extraction
- ⏳ Install Pillow for image processing
- ⏳ Create PDF text extraction function
- ⏳ Create image-to-text OCR function
- ⏳ Implement fallback OCR for pages with <100 characters
- ⏳ Add text preprocessing and cleanup
- ⏳ Add retry mechanism with "higher resolution" option for OCR failures

### LLM Integration (GPT-4o)
- ⏳ Set up OpenAI API client
- ⏳ Create bill parsing prompt template
- ⏳ Implement field extraction JSON schema
- ⏳ Create first LLM call for field completion
- ⏳ Create second LLM call for confidence scoring
- ⏳ Add PII masking before sending to GPT (addresses, etc.)
- ⏳ Implement <32k token limit handling

### Data Processing Pipeline
- ⏳ Create heuristic field grab (regex for money/dates)
- ⏳ Implement date normalization (ISO-8601)
- ⏳ Implement currency normalization (¢ precision)
- ⏳ Add confidence threshold logic (0.9 for needs-review)
- ⏳ Create vendor-alias lookup table
- ⏳ Implement fallback categorization with GPT-4o
- ⏳ Add extracted data validation
- ⏳ Add inline quick-edit functionality for vendor corrections
- ⏳ Implement feedback loop to alias table for learning

---

## Phase 4: API Development

### Bill Management APIs
- ⏳ `GET /api/v1/bills/{id}` - Get single bill
- ⏳ `PATCH /api/v1/bills/{id}` - Update bill (manual corrections)
- ⏳ `GET /api/v1/bills` - List bills with pagination
- ⏳ `DELETE /api/v1/bills/{id}` - Delete bill
- ⏳ Add bill search endpoint with filtering
- ⏳ Add bill file download endpoint

### Category Management APIs
- ⏳ `GET /api/v1/categories` - List all categories
- ⏳ `POST /api/v1/categories` - Create new category
- ⏳ `PATCH /api/v1/categories/{id}` - Update category
- ⏳ `DELETE /api/v1/categories/{id}` - Soft delete category (archive)
- ⏳ Add category validation (unique names)
- ⏳ Implement cascade updates for category renames

### Analytics & Insights APIs
- ⏳ Create spending analytics endpoint
- ⏳ Calculate YTD totals by category
- ⏳ Calculate highest monthly spend
- ⏳ Calculate average spend per category
- ⏳ Generate payment trend data for charts
- ⏳ Create next due date calculations

### User Journey API Requirements
- ⏳ Add JWT expiry handling with client-side retry logic
- ⏳ Implement queue persistence for mid-upload auth failures
- ⏳ Add time-to-value (TTV) tracking (<60 seconds target)
- ⏳ Create endpoint for bulk upload status tracking

---

## Phase 5: Frontend Development

### Design System Foundation
- ⏳ Create `tokens.css` with all color, spacing, typography custom properties
- ⏳ Implement CSS custom properties for spacing scale (--space-0 through --space-8)
- ⏳ Define color palette CSS variables (Ink #222, Graphite #666, Paper #F8F9FA)
- ⏳ Set up system font stack in CSS
- ⏳ Create elevation/shadow system (Shadow-100, Shadow-200)
- ⏳ Implement BEM naming convention across all components
- ⏳ Set up CSS file structure with proper ordering (imports, reset, layout, components, utilities)

### Basic HTML/CSS Framework
- ⏳ Create `index.html` with single-page app structure
- ⏳ Set up CSS Grid + Flexbox layout system
- ⏳ Implement responsive grid (12-col desktop, 8-col tablet, 1-col mobile)
- ⏳ Create core CSS classes (.card, .btn-primary, .chart-container, .sidebar)
- ⏳ Add system font stack configuration
- ⏳ Implement responsive breakpoints (600px, 1024px)
- ⏳ Create color scheme (#222 primary, #666 secondary)

### Component Library Implementation
- ⏳ Create button variants (Primary, Secondary, Danger) with proper styling
- ⏳ Implement card component with Shadow-100 and proper padding
- ⏳ Create sidebar category item component with active states
- ⏳ Implement badges & chips with 12px border-radius and accent colors
- ⏳ Create form input styling with focus rings and proper labels
- ⏳ Design table component with hover states and proper row heights
- ⏳ Implement modal/drawer components with backdrop and positioning
- ⏳ Create toast notification system with proper positioning and timing

### Typography Implementation
- ⏳ Implement typography scale (H1-H3, Body1-2, Caption, Mono)
- ⏳ Add proper font weights and line heights per style guide
- ⏳ Implement text ellipsis for long vendor names
- ⏳ Add letter-spacing for different text roles
- ⏳ Ensure sentence-case capitalization for buttons and chips

### Authentication UI
- ⏳ Create login page (`/login`)
- ⏳ Add centered card layout with logo (max-width 400px, Shadow-200)
- ⏳ Implement email + password inputs with proper styling
- ⏳ Add gradient primary button (#111111 → #444444)
- ⏳ Implement email validation on blur with card shake animation
- ⏳ Connect to authentication API
- ⏳ Add form validation and error handling
- ⏳ Implement JWT storage and management
- ⏳ Add "Forgot?" link placeholder for future password reset
- ⏳ Implement expired JWT redirect handling with inline notice
- ⏳ Add hero demo GIF with 8s auto-loop on landing
- ⏳ Create "Try It Now" CTA with Primary button styling

### Dashboard Home Page
- ⏳ Create sticky header (64px height) with logo and "Add Bill" button
- ⏳ Implement left rail category navigation (240px fixed width on desktop)
- ⏳ Add scrollable category list (>6 items) with proper styling
- ⏳ Create hero category card design matching reference
- ⏳ Integrate D3.js for payment trend charts with proper styling
- ⏳ Add three summary cards (Last Payment, Next Due, YTD)
- ⏳ Create important documents list with icons and proper table styling
- ⏳ Add view/download buttons for documents
- ⏳ Implement empty state with illustration and "Upload your first bill" CTA
- ⏳ Add count-up animation for YTD card after successful uploads
- ⏳ Create dismissible "?" beacon on chart legend for first session
- ⏳ Add pulse effect for newly processed files in document list
- ⏳ Implement hero card animation (400ms ease-out) for trend chart stroke

### File Upload Interface
- ⏳ Create drag-and-drop file upload zone
- ⏳ Add file selection dialog fallback
- ⏳ Implement file type validation (PDF, PNG, JPG)
- ⏳ Show processing skeleton cards with proper animation
- ⏳ Add upload progress indicators
- ⏳ Display success/error states with toast notifications
- ⏳ Connect to WebSocket for real-time updates
- ⏳ Add "Safe to close tab — we'll notify you" subtitle during processing
- ⏳ Implement multi-file support with tip: "you can multi-select files"
- ⏳ Add "Browse Files" secondary CTA for Safari DataTransfer bug
- ⏳ Create processing cards that animate into completion with checkmark

### Bill Detail Page
- ⏳ Create back arrow navigation in top bar
- ⏳ Implement two-column layout (responsive)
- ⏳ Add editable form for extracted fields with proper styling
- ⏳ Embed PDF viewer component (16:21 aspect ratio)
- ⏳ Add "Edit metadata" toggle with opacity fade transition (120ms)
- ⏳ Connect to bill update API
- ⏳ Add field validation and saving functionality
- ⏳ Implement needs-review banner with yellow borders for low-confidence fields
- ⏳ Add auto-focus to first invalid field in needs-review state
- ⏳ Create "Bill confirmed. Thank you!" toast on needs-review completion
- ⏳ Add pinch-zoom and "Open full-screen" action for mobile PDF viewing

### Category Management UI
- ⏳ Create category modal dialog with proper styling
- ⏳ Add name input field with validation
- ⏳ Implement color picker (hex values) component
- ⏳ Add save/cancel buttons with disabled states
- ⏳ Implement drawer pattern on mobile (slide up from bottom)
- ⏳ Connect to category APIs
- ⏳ Add category deletion confirmation
- ⏳ Handle category rename cascading
- ⏳ Add + icon in sidebar footer for new categories
- ⏳ Implement auto-scroll and highlight for new categories
- ⏳ Add pre-filled input with auto-select text for category rename
- ⏳ Replace "Delete" with "Archive" terminology for non-destructive operations
- ⏳ Add live-update of sidebar swatch and chart stroke via CSS variables

### Search & Filter Interface
- ⏳ Create global search bar with proper styling
- ⏳ Implement 300ms debounce functionality
- ⏳ Add search results table with sticky sub-header
- ⏳ Display vendor, amount, due date, category badge in table
- ⏳ Make rows clickable to bill detail with hover states
- ⏳ Add filter options by category/date
- ⏳ Ensure ≤150ms search latency
- ⏳ Implement space key selection for table rows
- ⏳ Add "/" keyboard shortcut to focus search
- ⏳ Show current query and result count in sticky sub-header

### Way-finding & Micro-copy Implementation
- ⏳ Add tooltip system (600ms delay, 8px offset, 240px max-width)
- ⏳ Implement progressive disclosure for advanced options
- ⏳ Add "?" keyboard shortcut for cheat-sheet overlay
- ⏳ Create consistent empty state pattern (what, why, action)
- ⏳ Add micro-copy library with helpful tips and guidance
- ⏳ Implement toast stacking limit (max 3) with role="alert"
- ⏳ Add warning states (yellow) 7 days before due dates

---

## Phase 6: Advanced Features

### Data Visualization (D3.js)
- ⏳ Install and configure D3.js
- ⏳ Create D3 helper module with default theme and tooltip utility
- ⏳ Create payment trend line chart with category accent colors (2px stroke)
- ⏳ Add interactive hover states with tooltip (Date & Amount, 12px above point)
- ⏳ Implement responsive chart sizing (16:9 ratio)
- ⏳ Add chart legends and axes with proper styling
- ⏳ Create category spending breakdowns
- ⏳ Add time range selectors
- ⏳ Implement gridlines (#EEEEEE, 1px, vertical hidden by default)
- ⏳ Add area fills (4% opacity accent) for selected category
- ⏳ Add mobile tap highlights (3s duration)
- ⏳ Implement tick label rotation (45° below 500px width)

### Icon System Implementation
- ⏳ Install Lucide icons library
- ⏳ Create SVG icon sprites from Lucide subset (24px artboard)
- ⏳ Implement 1.5px stroke width for icons
- ⏳ Ensure 36×36px minimum tap targets
- ⏳ Add semantic recoloring for Error/Success contexts only

### Motion & Micro-Interactions
- ⏳ Implement button press animation (120ms, cubic-bezier(.4,0,.2,1))
- ⏳ Add modal enter/exit transitions (240ms)
- ⏳ Create sidebar expand/collapse animation (180ms ease-out)
- ⏳ Add chart point hover grow effect (100ms linear)
- ⏳ Ensure animations only use transform & opacity (preserve text crispness)

### Settings & Configuration
- ⏳ Create settings page with accordion layout
- ⏳ Add profile management section
- ⏳ Implement storage path configuration with browse button
- ⏳ Add LLM API key management with show/hide functionality
- ⏳ Create beta feature toggles
- ⏳ Add data export functionality
- ⏳ Implement accordion chevron rotation (90°) on open
- ⏳ Add warning dialog for unwritable storage paths

### Error Handling & User Experience
- ⏳ Create 404 page with illustration (200px square) and "Go Home" secondary button
- ⏳ Add global error boundary
- ⏳ Implement loading states throughout app
- ⏳ Add offline detection and messaging
- ⏳ Create user feedback notifications (toast system)
- ⏳ Add keyboard navigation support (tabindex, focus order)

### Delight Features & Viral Loops
- ⏳ Implement count-up animation on YTD card after uploads
- ⏳ Add confetti animation (one-time 🎉) after paywall purchase
- ⏳ Create "Import from Gmail" teaser with "Coming Soon 🔒"
- ⏳ Design share feature preview for anonymized spending infographics
- ⏳ Add social share card generation capability

---

## Phase 7: Testing & Quality Assurance

### Backend Testing
- ⏳ Create unit tests for data models
- ⏳ Add API endpoint tests
- ⏳ Test file upload functionality
- ⏳ Validate OCR pipeline accuracy
- ⏳ Test LLM integration and error handling
- ⏳ Add authentication and security tests
- ⏳ Test database operations and migrations

### Frontend Testing
- ⏳ Create component-level tests
- ⏳ Test user interaction flows
- ⏳ Validate responsive design (600px, 1024px breakpoints)
- ⏳ Test accessibility compliance (WCAG 2.1 AA)
- ⏳ Add browser compatibility testing
- ⏳ Test file upload and processing flows
- ⏳ Validate color contrast ≥4.5:1 for text <18pt
- ⏳ Test aria-label and aria-live implementations
- ⏳ Verify focus order follows visual order

### Integration Testing
- ⏳ Test complete upload-to-dashboard flow
- ⏳ Validate WebSocket real-time updates
- ⏳ Test category management workflows
- ⏳ Validate search and filtering accuracy
- ⏳ Test data visualization rendering
- ⏳ Performance testing (300ms page load target)

### User Journey Testing
- ⏳ Run usability test with "Jessica" persona (ensure TTV < 60s)
- ⏳ Confirm needs-review flow resolves in ≤3 clicks
- ⏳ Stress-test with 1000 bills (scrolling & search ≤150ms)
- ⏳ Verify copy length vs grid constraints (no truncation)
- ⏳ Test all blind-spot mitigations from user journey
- ⏳ Validate all micro-copy and way-finding patterns

---

## Phase 8: Performance & Optimization

### Backend Optimization
- ⏳ Optimize database queries and indices
- ⏳ Implement caching for frequent operations
- ⏳ Add request rate limiting
- ⏳ Optimize file storage and retrieval
- ⏳ Monitor and optimize LLM API usage
- ⏳ Add database connection pooling

### Frontend Optimization
- ⏳ Minimize CSS and JavaScript bundles
- ⏳ Implement lazy loading for images
- ⏳ Optimize chart rendering performance
- ⏳ Add service worker for caching
- ⏳ Compress and optimize assets
- ⏳ Implement virtual scrolling for large lists

---

## Phase 9: Security & Privacy

### Security Implementation
- ⏳ Add input sanitization throughout app
- ⏳ Implement CSRF protection
- ⏳ Add rate limiting to prevent abuse
- ⏳ Secure file upload validation
- ⏳ Add audit logging for sensitive operations
- ⏳ Implement secure session management

### Privacy Features
- ⏳ Add PII masking in logs
- ⏳ Implement data retention policies
- ⏳ Add file auto-deletion settings
- ⏳ Create data export functionality
- ⏳ Add privacy policy and terms
- ⏳ Implement user data deletion

---

## Phase 10: Future-Proofing Hooks

### Paywall Infrastructure
- ⏳ Create paywall page (`/pay`) with marketing copy (H2, body1)
- ⏳ Add pricing card with Shadow-200 styling
- ⏳ Integrate Stripe Checkout placeholder with hosted checkout style
- ⏳ Add `ENABLE_PAYWALL` environment flag
- ⏳ Implement redirect middleware for unauthenticated users
- ⏳ Add preview screen with blur overlay + "Requires Pro" badge
- ⏳ Implement webhook for `is_paid = true` flag updates

### Gmail Integration Preparation
- ⏳ Create IMAP connection framework
- ⏳ Add email parsing task structure
- ⏳ Design email forwarding workflow
- ⏳ Create email attachment processing
- ⏳ Add email-to-bill conversion logic

### Multi-Tenant Preparation
- ⏳ Design tenant isolation in database
- ⏳ Create tenant management models
- ⏳ Add `MULTI_TENANT` environment flag
- ⏳ Prepare database migration scripts
- ⏳ Design tenant-based file storage

### Negotiation Agent Hooks
- ⏳ Create `Advice` table for suggestions
- ⏳ Design micro-service communication pattern
- ⏳ Add suggestion display UI components
- ⏳ Create bill analysis framework
- ⏳ Add negotiation tracking models

---

## Phase 11: Documentation & Deployment

### Documentation
- ⏳ Complete API documentation (Swagger)
- ⏳ Create user guide and tutorials
- ⏳ Write developer setup instructions
- ⏳ Document configuration options
- ⏳ Create troubleshooting guide
- ⏳ Add code comments and docstrings

### Deployment Preparation
- ⏳ Finalize Docker Compose configuration
- ⏳ Create production environment variables
- ⏳ Set up database backup strategy
- ⏳ Add health monitoring endpoints
- ⏳ Create deployment scripts
- ⏳ Add logging and monitoring configuration

### Final Polish
- ⏳ Review and test complete user journeys
- ⏳ Optimize loading and transition animations
- ⏳ Add helpful error messages and guidance
- ⏳ Test edge cases and error scenarios
- ⏳ Validate against PRD requirements
- ⏳ Conduct final security review
- ⏳ Validate style guide compliance across all pages
- ⏳ Verify all user journey touchpoints and micro-interactions
- ⏳ Test all personas (Jessica, Raj, Sam) user flows

---

## Current Status Summary
- **Total Tasks**: 240+ items across 11 phases
- **Completed**: 0 ✅
- **In Progress**: 0 🚧  
- **Pending**: All ⏳

## Next Recommended Action
🎯 **Start with Phase 1**: Begin by initializing the Git repository and setting up the basic project structure. This provides the foundation for all subsequent development.

**Specifically, tackle**: "Initialize Git repository with proper `.gitignore`" as the very first task.
