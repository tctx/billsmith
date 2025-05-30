# BillSmith User Journey Map

**Purpose**: Provide an exhaustive, step‑by‑step narrative of how a real‑world user interacts with BillSmith from the first marketing touch through day‑to‑day use.

**Audience**: Autonomous AI engineers and PM bots Joe & Brian.

**Sources**: PRD, Development Checklist, UI & UX Style Guide.

## 1. Personas & Mental Models

### User Personas

1. **"Jessica the Home‑Renter"**
   - **Context & Goals**: Pays 6+ utility bills; tired of digging through e‑mails. Wants a single source of truth and reminders.
   - **Primary KPIs**: Weekly active use, zero late fees.

2. **"Raj the Small‑Biz Owner"** (stretch)
   - **Context & Goals**: Tracks utilities + SaaS invoices; worried about tax season. Needs exportable data & category control.
   - **Primary KPIs**: CSV exports, category CRUD.

3. **"Sam the Power User"**
   - **Context & Goals**: Early adopter who uploads 10 years of past PDFs. Evaluates data viz; posts on Hacker News.
   - **Primary KPIs**: Retention after bulk‑upload, shares/mentions.

### Mental Model Insight
Users equate bills with tasks. They feel relief when a task is "closed." Every micro‑interaction should reinforce progression toward "✅ Paid / Archived."

## 2. End‑to‑End Journey Phases

### Journey Overview
1. **Awareness & Landing**
2. **Account Creation / Login**
3. **First‑Time Upload & Processing**
4. **Dashboard Comprehension**
5. **Routine Monthly Use**
6. **Exceptional Paths** (Needs‑Review, Errors)
7. **Management & Customisation** (Categories, Settings)
8. **Future Upsell** (Paywall, Negotiation Agent)

*Each phase below details User Actions → System Responses → Emotional State → UX Cues → Blind‑Spot Mitigation.*

### 2.1 Awareness & Landing

| Step | Details |
|------|---------|
| **A‑1** | User clicks an ad/blog/HN post → lands on `/login` (marketing copy optional flag). |
| **A‑2** | Hero headline "One inbox for every bill." Sub‑copy spells out "Drag & drop, we do the rest." |

#### UX Cues
- Hero demo GIF auto‑loops once (8 s max).
- CTA = "Try It Now" Primary button.

#### Blind‑spots
- **Risk**: Over‑promise extraction accuracy. 
- **Mitigation**: micro‑copy "99% accuracy — verify unusual bills."

### 2.2 Account Creation / Login

| Step | System | Emotion | Cues |
|------|--------|---------|------|
| **B‑1** | User enters email → inline validation | Confidence | Shows green check ✔︎ next to field |
| **B‑2** | JWT issued, redirect `/` | Relief / novelty | Header skeleton fades in |

#### System Responses
- Shadow‑200 card shakes on invalid submit (120 ms).
- Skeleton screen uses neutral gray blocks.

#### Blind‑spots
**Forgotten password flow** not in MVP; add "Forgot?" link placeholder.

### 2.3 First‑Time Upload & Processing

| # | User Action | System Reaction | Emotional Check | Way‑finding |
|---|-------------|-----------------|-----------------|-------------|
| **C‑1** | Drags 3 PDFs onto drop‑zone | Each file card animates into "Processing" with spinner | Excited but anxious | Subtitle "Safe to close tab — we'll notify you." |
| **C‑2** | Back‑end posts WebSocket update done | Card swaps to ✓ plus "View" link | Satisfaction | Toast: "3 bills processed successfully." |
| **C‑3** | One bill < 0.9 confidence | Card badge Needs‑Review (yellow) | Mild worry | Tooltip "Click to confirm totals." Focus ring guides them. |

#### Blind‑spots
- **Risk**: Large 30 MB scans may stall. 
- **Mitigation**: progress % per file, fail‑fast 50 MB hard limit.

### 2.4 Dashboard Comprehension

**Sequence** (once at least one bill exists):

1. **Hero Card** announces current category (first in list).
2. **Trend Chart** animates stroke (400 ms ease‑out).
3. **Summary cards** count up from 0 → value (count‑up.js like effect).
4. **Important Docs table** shows last three bills; subtle pulse effect on newly processed file.

#### UX Cues
**First session only**: show a dismissible `?` beacon on chart legend: "Click any point to inspect amount."

#### Blind‑spots
- **Risk**: Empty dashboard looks barren. 
- **Mitigation**: Provide empty state illustration + "Upload your first bill" call‑to‑action.

### 2.5 Routine Monthly Use

| Routine | Positive Pods | Micro‑copy |
|---------|---------------|------------|
| **Upload new bills** | Drag‑and‑drop or "Add Bill" button always visible in header | "Tip: you can multi‑select files." |
| **Monitor upcoming dues** | Next‑Due summary turns warning yellow 7 days before. | "Rent due in 7 days – pay on time, avoid fees." |
| **Search past invoices** | Instant results with keyboard nav | "Press / to focus search." |
| **Add a category** | + icon in sidebar footer | Autoscrolls list, highlights new category. |

### 2.6 Exceptional Paths

#### Needs‑Review Flow
1. User enters bill detail → banner: "We couldn't verify the total with high confidence."
2. Highlighted fields show yellow border; first invalid field auto‑focus.
3. On save, toast "Bill confirmed. Thank you!"; badge disappears.

#### Error States
- **OCR failure** → red badge "OCR Error". Provide "Retry with higher resolution?" link.
- **401 JWT expired** → redirect `/login?expired=1` with inline notice.

### 2.7 Management & Customisation

| Feature | Flow | Cues |
|---------|------|------|
| **Rename Category** | Click ⋯ menu → "Rename" | Input pre‑filled, auto‑select text. |
| **Change Storage Path** | Settings > Storage → "Choose folder" | Warn dialog if path exists but unwritable. |
| **Color Update** | Hex picker live‑updates sidebar swatch + chart stroke via CSS variable. | |

### 2.8 Future Paywall Flow

1. User hits feature flag (e.g., "Insights" page).
2. Middleware redirects `/pay` → pricing.
3. After Stripe success, webhook flips `is_paid = true`; user returned with confetti (one‑time 🎉).
4. "Insights" now unlocked.

#### UX Risk
- **Risk**: Confusion if they click Insights accidentally. 
- **Mitigation**: preview screen with blur overlay + "Requires Pro" badge.

## 3. Touchpoint Blueprint (JJG five‑plane overlay)

| Plane | Key Decisions |
|-------|---------------|
| **Surface** | Minimalist cards, high‑contrast typography (Style Guide §1). |
| **Skeleton** | 12‑column grid desktop; responsive breakpoints (Style Guide §2). |
| **Structure** | Clear IA: Dashboard → Bill Detail → Settings / Categories. |
| **Scope** | MVP upload/search/manage; hooks for Paywall & Gmail ingest. |
| **Strategy** | Reduce time‑to‑value (TTV) to < 60 seconds from first visit to extracted data. |

## 4. Way‑finding Patterns & Micro‑copy Library

### Interface Patterns
- **Empty States**: Always contain what, why, and a primary action.
- **Tooltips**: Delay 600 ms on hover; place 8 px offset; max‑width 240 px.
- **Toasts**: Never more than 3 stacked; auto‑dismiss 5 s; `role="alert"`.
- **Progressive Disclosure**: Advanced options hidden behind "Show advanced" links.
- **Keyboard Shortcuts**: `/` focus search, `?` opens cheat‑sheet overlay.

## 5. Blind‑Spots & Mitigations

| Risk | Why it Hurts | Proposed Fix |
|------|--------------|--------------|
| **Long OCR wait > 30 s** | User thinks app froze | Show per‑file progress %, fallback SMS/email notification. |
| **Mis‑categorised vendor** | Breaks YTD totals | Allow quick‑edit inline + feedback loop to alias table. |
| **Deleting a category w/ bills** | Data loss anxiety | Replace "Delete" with "Archive"; explain non‑destructive. |
| **Mobile PDF readability** | 16:21 viewer may be illegible | Offer "Open full‑screen" action + pinch‑zoom. |
| **JWT expiry mid‑upload** | Upload fails silently | Retain queued files client‑side, retry after re‑auth. |
| **Multi‑file drag on Safari** | DataTransfer bug | Provide "Browse Files" secondary CTA. |

## 6. Delight & Viral Loops

### Delight Features
- **Count‑Up Animation** on YTD card after each successful upload.
- **Share Feature Preview** (Post‑MVP): generate anonymised spending infographics; social share card.
- **"Import from Gmail" Teaser**: Disabled setting with "Coming Soon 🔒"; collects email captures.

## 7. Journey Timeline (Text Diagram)

```
Landing → Login → Dashboard (empty) → Upload Wizard → Processing →
Needs‑Review? (branch) → Dashboard (populated) → Routine Monthly Loop
    ↘ Settings / Categories ↘ Search / Detail ↘ Exceptional States ↘ Paywall (future)
```

## 8. Hand‑off Checklist for Joe & Brian 🗂️

- ✅ Verify copy length vs. grid constraints (no truncation).
- ✅ Run usability test with "Jessica" persona; ensure TTV < 60 s.
- ✅ Confirm Needs‑Review flow resolves in ≤ 3 clicks.
- ✅ Stress‑test with 1000 bills; scrolling & search must remain ≤ 150 ms.
- ✅ Validate WCAG AA contrast on accent palettes.
- ✅ Re‑review blind‑spots after Sprint 2; add tasks to Development Checklist.

## 9. Appendix

### Future Considerations
- Flow variants for multi‑tenant & Gmail ingest (deferred).
- Negotiation agent task injection points (deferred).
- Stripe refund edge cases.