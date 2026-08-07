# Sprint 03 - Routing and User Flow

## Objective

Create the main application routes and user flow for Laterite Comparator — Grade Control (LCGC).

The goal is to make the application feel navigable and ready for the next sprint: real camera and result flow.

---

## Scope

Allowed to create or modify:

- frontend/app/page.tsx
- frontend/app/scan/page.tsx
- frontend/app/result/page.tsx
- frontend/app/history/page.tsx
- frontend/app/settings/page.tsx
- frontend/components/layout/*
- frontend/components/home/*
- frontend/components/scan/*
- frontend/components/result/*
- frontend/components/history/*
- frontend/components/settings/*
- frontend/types/*
- frontend/constants/*

Do NOT modify:

- frontend/app/globals.css
- frontend/app/layout.tsx
- frontend/package.json
- frontend/.env.local
- AGENTS.md
- docs/*

Do NOT install new packages.

---

## Required Routes

Create or update these App Router pages:

- /
- /scan
- /result
- /history
- /settings

---

## Required User Flow

### Home Page

- Capture Material button navigates to `/scan`
- Upload Image button also navigates to `/scan` for now
- Bottom navigation:
  - Home → `/`
  - History → `/history`
  - Settings → `/settings`

Use Next.js `Link` or `useRouter`.

Do NOT use `window.location`.

---

### Scan Page

Create a mobile-first scan page.

Display:

- Header / back navigation
- Camera placeholder card
- Scanner frame overlay
- Instruction text:
  "Position the laterite material inside the frame."
- Primary button:
  "Analyze Material"
- Secondary button:
  "Upload Image"

For now:

- Analyze Material navigates to `/result`
- Upload Image does not need real upload logic yet

---

### Result Page

Create a dummy result page that represents the final LCGC result experience.

Display:

1. Similarity score
2. Confidence label
3. User photo placeholder vs comparator photo placeholder
4. Material summary
5. QAQC cards
6. Dynamic description cards
7. Alternative matches
8. Scan Again button

Important:

The result page must emphasize comparison.

Text principle:

"This scanned material is visually similar to comparator sample RB4-015."

Avoid absolute classification wording.

---

### History Page

Create a simple dummy history page.

Display three scan history cards:

- thumbnail placeholder
- material code
- similarity
- date

---

### Settings Page

Create a simple settings page.

Display:

- App Name: Laterite Comparator
- Edition: Grade Control
- Version: MVP 0.1
- Data Source: Local Comparator Database
- Theme: Dark Industrial

---

## Dummy Result Data

Use this dummy data:

Best Match:

- Code: RB4-015
- Zone: Earthy Saprolite
- Color: Brown Greenish
- Similarity: 98.7%
- Confidence: Very High
- Ni: 1.82
- Co: 0.08
- Fe: 23.41
- MgO: 9.62
- SiO2: 41.20

Description attributes:

- Zona: Earthy Saprolite
- Warna: Brown Greenish
- Ukuran: Gravel - Boulder
- Komposisi: Serpentine, Goethite, Garnierite traces
- Keterangan: Weathered ultramafic material with greenish brown tone and earthy texture.

Alternative Matches:

- RB4-011 — 95.4%
- RB4-007 — 93.8%
- RB4-021 — 91.2%

---

## UI Requirements

Follow:

- AGENTS.md
- docs/design_system.md

Style:

- Dark industrial
- Mobile first
- Premium mining application
- High contrast
- Large touch targets
- Card-based UI

---

## Component Rules

Do not put everything inside page.tsx.

Create reusable components when needed.

Recommended components:

- ScanHeader
- ScanFrame
- AnalyzeActions
- ResultHero
- ImageComparison
- QaqcCard
- DescriptionCard
- AlternativeMatchCard
- HistoryCard
- SettingsCard

---

## Acceptance Criteria

Sprint 03 is complete if:

- `/` opens homepage
- `/scan` opens scan page
- `/result` opens result page
- `/history` opens history page
- `/settings` opens settings page
- Capture Material button navigates to `/scan`
- Analyze Material button navigates to `/result`
- Scan Again button navigates to `/scan`
- Bottom navigation works
- Result page shows user image vs comparator image
- No backend or AI code is added
- No package is installed
- App runs without error