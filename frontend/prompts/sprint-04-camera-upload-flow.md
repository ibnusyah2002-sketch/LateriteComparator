# Sprint 04 - Camera and Upload Flow

## Objective

Implement the first real image input flow for Laterite Comparator — Grade Control (LCGC).

The goal is to allow users to:
1. Open the scan page.
2. Activate browser camera.
3. Capture a material image.
4. Preview the captured image.
5. Upload an image from device storage.
6. Continue to result page using the captured or uploaded image as temporary local preview data.

This sprint does NOT implement backend, AI, Supabase, or OpenCLIP yet.

---

## Scope

Allowed to create or modify:

- frontend/app/scan/page.tsx
- frontend/app/result/page.tsx
- frontend/components/scan/*
- frontend/components/result/*
- frontend/hooks/useCamera.ts
- frontend/services/camera.ts
- frontend/types/scan.ts
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

## Camera Requirements

Use native browser APIs only:

- navigator.mediaDevices.getUserMedia
- video element
- canvas capture

Camera behavior:

- On scan page load, show a button:
  "Start Camera"

- When clicked:
  - request camera permission
  - use environment-facing camera if available
  - show live camera preview inside scanner frame

- Add button:
  "Capture Image"

- When clicked:
  - capture current video frame to canvas
  - convert to image data URL
  - show captured preview

- Add button:
  "Retake"

- Retake should reset captured image and return to live camera preview.

---

## Upload Requirements

Add secondary button:

Upload Image

Use input type file:

- accept image/*
- when image selected:
  - read as data URL
  - show image preview
  - disable live camera preview if needed

---

## Analyze Flow

After image is captured or uploaded:

Show primary button:

Analyze Material

When clicked:

- save temporary image data in sessionStorage using key:
  lcgc_current_scan_image

- navigate to:
  /result

Do not send image to backend yet.

---

## Result Page Temporary Preview

Update result page:

- if sessionStorage has lcgc_current_scan_image:
  - display it as User Photo
- if not:
  - show placeholder user image

Comparator image can remain placeholder for now.

---

## Error Handling

Handle:

- camera permission denied
- camera not available
- capture before camera ready
- invalid uploaded file

Show clear friendly messages.

Example:

"Camera access is required to scan material."

---

## UI Requirements

Follow:

- AGENTS.md
- docs/prd.md
- docs/design_system.md

Style:

- Dark industrial
- Mobile first
- Large touch targets
- Scanner frame must remain visible
- Captured/uploaded preview must feel premium

---

## Component Suggestions

Create or update components:

- CameraScanner
- CameraPermissionState
- ImagePreview
- UploadImageButton
- ScanActions

Use hooks:

- useCamera

Use services:

- camera.ts

---

## Code Quality

Use TypeScript.

Do not place all logic inside page.tsx.

Do not use external camera libraries.

Do not install packages.

Keep browser-only code inside client components.

Use "use client" where needed.

---

## Acceptance Criteria

Sprint 04 is complete if:

- /scan opens without error
- Start Camera requests permission
- Camera preview appears
- Capture Image works
- Captured image preview appears
- Retake works
- Upload Image works
- Analyze Material navigates to /result
- /result displays uploaded/captured user image
- App runs without terminal errors