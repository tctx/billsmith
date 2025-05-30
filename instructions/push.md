# Push Guidelines for Billsmith

Use this file as the single source of truth for how the AI (or any developer) should phrase every commit message pushed to GitHub.

## 1. Commit Message Format

```
<one-line subject in imperative, ≤50 chars>

<blank line>
- <bullet 1 in imperative>
- <bullet 2>
- <...>

<optional footers>
```

### Rules
- Imperative voice (e.g., add, fix, refactor). Avoid past tense.
- One idea per bullet. Keep bullets ≤72 chars.
- List bullets in top-down order: feature → implementation → tests → docs.
- If you close an issue, add a footer like `Closes #12`.

## 2. Map to Checklist

When possible, prefix bullets with the matching Checklist section (e.g., `Core Data Model:`) so progress is traceable.

## 3. Examples

### Example 1: Initial Setup
```
start ingest prototype and data layer

- Core Data Model: add sqlite schema for feeds and videos
- CLI: implement feeds add|list commands
- Tests: add basic unit test for adapter discover
- Docs: update README with setup commands

Closes #3
```

### Example 2: Feature Addition
```
add ffmpeg normaliser job and event emission

- Download Pipeline: create Cloud Run ffmpeg job
- Dedup: compute SHA-256, skip existing hash
- Events: publish video.ready on success
- Tests: integration test happy path
```

## 4. Push Workflow

1. `git add ...`
2. `git commit` – follow the format above
3. `git push origin <branch>`
4. Open a PR describing why (link to Checklist/PRD). Title can copy the subject line.

That's it—consistent, machine-friendly, and human-readable.