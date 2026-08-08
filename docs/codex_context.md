# Codex Context - LCGC

## Project Name

LCGC — Laterite Comparator for Grade Control

Application name:
Laterite Comparator

Tagline:
Scan. Compare. Identify.

---

## Product Principle

LCGC is an AI Comparator, not an AI classification system.

The app should say:

"This scanned material is visually similar to comparator sample RB4-015."

The app should avoid:

"This material is definitely Earthy Saprolite."

The system compares visual similarity between the scanned material image and comparator database samples.

---

## Current Project Stage

Frontend MVP is in progress.

Completed:

- Project structure
- Git repository setup
- Local database ignored from Git
- AGENTS.md
- PRD
- Design system
- Homepage production UI
- Routing flow
- Dummy scan page
- Dummy result page
- Dummy history page
- Dummy settings page

Current next sprint:

Sprint 04 — Camera and Upload Flow

Sprint 04 has not been implemented yet.

---

## Tech Stack

Frontend:

- Next.js App Router
- React
- TypeScript
- Tailwind CSS
- Lucide React

Backend planned:

- FastAPI
- Python
- Supabase PostgreSQL
- Supabase Storage
- pgvector

AI planned:

- OpenCV
- OpenCLIP embeddings
- Vector similarity search

---

## Important Project Folders

Root:

- frontend
- backend
- ai
- database
- dataset
- docs
- prompts

Frontend:

- frontend/app
- frontend/components
- frontend/hooks
- frontend/services
- frontend/types
- frontend/constants
- frontend/public

---

## Protected Files and Folders

Do not modify unless explicitly instructed:

- frontend/app/globals.css
- frontend/app/layout.tsx
- frontend/package.json
- frontend/.env.local
- AGENTS.md
- docs/*
- database/*
- dataset/*

Do not commit:

- database/*
- dataset/*
- .env files
- node_modules
- .next

---

## Sprint 04 Goal

Implement the first real image input flow.

Required user flow:

1. Open /scan
2. Click Start Camera
3. Browser requests camera permission
4. Camera preview appears
5. User captures image
6. Captured image preview appears
7. User can retake image
8. User can upload image from device
9. User clicks Analyze Material
10. Image is saved temporarily to sessionStorage
11. App navigates to /result
12. Result page displays the scanned/uploaded image as User Photo

---

## Sprint 04 Should Not Implement

Do not implement:

- Backend
- API route
- Supabase
- AI model
- OpenCLIP
- Real comparator image retrieval
- Database parsing
- Authentication
- Deployment

---

## Sprint 04 Allowed Files

Allowed to create or modify:

- frontend/app/scan/page.tsx
- frontend/app/result/page.tsx
- frontend/components/scan/*
- frontend/components/result/*
- frontend/hooks/useCamera.ts
- frontend/services/camera.ts
- frontend/types/scan.ts
- frontend/constants/*

Do not install new packages.

Use native browser APIs only:

- navigator.mediaDevices.getUserMedia
- video element
- canvas
- FileReader
- sessionStorage

---

## Codex Usage Rule

For now, Codex should only be used as:

- reviewer
- debugger
- second opinion
- code explainer

Codex should not edit files unless explicitly instructed.

Preferred Codex prompts:

"Review only. Do not modify files."

"Explain this error. Do not modify files."

"Suggest changes for this file only. Do not apply."

Avoid broad prompts:

"Implement Sprint 04."

"Fix all errors."

"Refactor the project."

"Make the app production ready."