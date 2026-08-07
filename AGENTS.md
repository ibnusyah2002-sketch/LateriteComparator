# AGENTS.md

# Project Identity

Project Name:
LCGC

Full Name:
Laterite Comparator for Grade Control

Product Name:
Laterite Comparator

Tagline:
Scan. Compare. Identify.

Purpose:
LCGC is a web-based AI Comparator for nickel laterite material identification. The application helps users compare a scanned material image with a validated comparator database and returns the most visually similar samples with descriptions and QAQC data.

Important:
LCGC is NOT an AI classification system.
LCGC is an AI Comparator system.

The system should always be designed around this principle:

User Image → Visual Analysis → Similarity Search → Comparator Result → QAQC + Description

---

# Development Role

You are acting as a senior software engineer working inside a production-oriented codebase.

You must:
- Follow existing project structure.
- Keep code modular.
- Avoid unnecessary rewrites.
- Avoid modifying unrelated files.
- Ask for confirmation before large architectural changes.
- Prefer small, safe, incremental changes.

---

# Tech Stack

Frontend:
- Next.js App Router
- React
- TypeScript
- Tailwind CSS

Backend:
- FastAPI
- Python

Database:
- Supabase PostgreSQL
- Supabase Storage
- pgvector

AI:
- OpenCV
- OpenCLIP
- Image embedding
- Visual similarity search

Deployment:
- Frontend: Vercel
- Backend: Railway
- Database and Storage: Supabase

---

# Folder Structure

Root project:

frontend/
backend/
ai/
database/
dataset/
docs/
assets/
prompts/
scripts/
testing/

Frontend structure:

frontend/app/
frontend/components/
frontend/components/home/
frontend/components/layout/
frontend/components/ui/
frontend/components/scan/
frontend/components/result/
frontend/components/history/
frontend/components/settings/
frontend/hooks/
frontend/services/
frontend/types/
frontend/constants/
frontend/lib/
frontend/public/

AI structure:

ai/models/
ai/preprocessing/
ai/embeddings/
ai/similarity/

---

# Naming Convention

Folders:
Use lowercase.

Examples:
components
services
constants
dataset
database

React Components:
Use PascalCase.

Examples:
CameraPreview.tsx
BottomNavigation.tsx
ResultCard.tsx

Utility files:
Use camelCase or kebab-case consistently.

Examples:
formatSimilarity.ts
imageProcessing.ts

Routes:
Use lowercase.

Examples:
/scan
/result
/history
/settings

Dataset image filenames:
Prefer lowercase file names.

Example:
rb4-015/front.jpg

Excel sample code may remain uppercase.

Example:
RB4-015

---

# Design System

Always follow:

docs/design_system.md

Main UI principles:
- Mobile first
- Dark industrial theme
- Premium appearance
- High contrast
- Field friendly
- Minimal text
- Large touch targets
- Scientific and professional feeling

Main colors:
Background: #0B0B0B
Surface: #161616
Primary Green: #2E7D32
Accent Green: #43A047
Border: #2A2A2A
Text Primary: #FFFFFF
Text Secondary: #A0A0A0

Do not introduce random new colors unless explicitly requested.

---

# UI Rules

The application must feel like a professional mining field application.

Home page must prioritize:
1. Camera preview
2. Capture action
3. Upload image
4. Recent scan history

Result page must prioritize:
1. Similarity score
2. User image vs comparator image
3. Material code
4. QAQC cards
5. Dynamic description cards
6. Alternative matches

Do not overload screens with text.

Prefer cards, badges, and visual hierarchy.

---

# Component Rules

Do not create large page files.

Page files should mostly compose components.

Good:
app/page.tsx imports Header, CameraPreview, ActionButtons, RecentScan, BottomNavigation.

Bad:
app/page.tsx contains hundreds of lines of JSX.

Create reusable components when UI appears more than once.

---

# Routing Rules

Use Next.js App Router.

Allowed core routes:
/ 
/scan
/result
/history
/settings
/admin

Use Next.js Link or useRouter for navigation.

Do not use window.location for internal navigation.

---

# Data Rules

Frontend must not hardcode final production comparator data.

Dummy data is allowed only for UI flow before backend integration.

All final material descriptions must come from the comparator database.

The result description should be dynamic.

Preferred response shape:

attributes: [
  { label: "Zona", value: "Saprolite" },
  { label: "Warna", value: "Brown Greenish" },
  { label: "Ukuran", value: "Gravel" },
  { label: "Komposisi", value: "Serpentine, Goethite" }
]

Frontend should render attributes dynamically.

---

# AI Rules

The AI system should not claim absolute material classification.

Correct phrasing:
"This scanned material is visually similar to comparator sample RB4-015."

Avoid:
"This material is definitely RB4-015."

Core AI pipeline:
Image upload
→ Image quality check
→ OpenCV preprocessing
→ OpenCLIP embedding
→ pgvector similarity search
→ Top 5 comparator result
→ Database description

---

# Backend Rules

FastAPI should handle:
- Image upload
- Image preprocessing
- Embedding generation
- Similarity search
- Result formatting

Backend should return structured JSON.

Do not put AI logic inside the frontend.

---

# Supabase Rules

Supabase will be used for:
- PostgreSQL data
- pgvector embeddings
- Image storage
- Authentication later

Do not expose secret keys in frontend.

Only NEXT_PUBLIC variables may be used in frontend.

Environment variables live in:
frontend/.env.local
backend/.env

---

# Security Rules

Never commit:
- .env.local
- .env
- API keys
- Supabase secret key
- private tokens
- large datasets

Use .gitignore.

---

# Git Rules

Use meaningful commit messages.

Format:

feat(ui): add homepage layout
feat(scan): add camera flow
feat(result): add comparator result screen
feat(api): add health endpoint
feat(ai): add image embedding service
fix(ui): improve responsive layout
docs: update design system

Avoid:
update
test
fix
coba

---

# Cursor Working Rules

Before making changes:
1. Read the relevant sprint prompt.
2. Read docs/design_system.md.
3. Summarize files to create or modify.
4. Explain assumptions.
5. Keep changes scoped.

Do not modify these files unless explicitly requested:
- globals.css
- app/layout.tsx
- package.json
- environment files

Do not install packages unless explicitly requested.

---

# Review Checklist

Before considering work complete:

- App runs without error.
- No unrelated files were modified.
- UI follows design system.
- Components are reusable.
- Routes work.
- TypeScript has no obvious errors.
- No secrets are committed.
- Code is understandable for a beginner developer.

---

# MVP Goal

The MVP must support this flow:

Open app
→ Camera or upload image
→ Analyze material
→ Show loading screen
→ Show best comparator match
→ Show user image vs comparator image
→ Show similarity score
→ Show QAQC cards
→ Show dynamic description
→ Show alternative matches
→ Save recent scan history

---

# Product Principle

Everything starts from comparison.

LCGC must always emphasize that it compares the scanned material with a validated laterite comparator database.