# Sprint 04 Readiness Review

## 1. Whether the project is ready for Sprint 04

The frontend is ready to start Sprint 04, but it is not ready to satisfy Sprint 04 yet.

Current readiness is good at the scaffold level:

- The required routes already exist, including `/scan` and `/result`.
- The scan page is already composed cleanly from small components.
- The result page already has the intended final layout structure.
- The existing dependency set is sufficient for Sprint 04 because native browser APIs can be used without installing anything new.

Current readiness is incomplete at the feature level:

- The `/scan` flow is still placeholder UI only.
- The `Analyze Material` action currently navigates directly to `/result` without requiring a captured or uploaded image.
- The upload button is not wired to a file input flow.
- The result page does not read `sessionStorage` yet.
- `frontend/hooks/useCamera.ts` and `frontend/services/camera.ts` are empty.
- `frontend/types/scan.ts` is too minimal for camera and upload state handling.

Conclusion:

Sprint 04 can be implemented safely on top of the current frontend structure, but the actual camera, upload, preview, temporary session storage, and result-image handoff are not implemented yet.

## 2. Files likely needed for Sprint 04

Most likely files to modify:

- `frontend/app/scan/page.tsx`
- `frontend/app/result/page.tsx`
- `frontend/components/scan/scan-frame.tsx`
- `frontend/components/scan/analyze-actions.tsx`
- `frontend/components/result/image-comparison.tsx`
- `frontend/hooks/useCamera.ts`
- `frontend/services/camera.ts`
- `frontend/types/scan.ts`

Likely new files within allowed scope:

- `frontend/components/scan/CameraScanner.tsx`
- `frontend/components/scan/CameraPermissionState.tsx`
- `frontend/components/scan/ImagePreview.tsx`
- `frontend/components/scan/UploadImageButton.tsx`
- `frontend/components/scan/ScanActions.tsx`
- `frontend/constants/scan.ts`

Supporting context from the current codebase:

- `/scan` already composes `ScanHeader`, `ScanFrame`, and `AnalyzeActions`.
- `/result` already composes the result hero, comparison, QAQC, description, and alternative match sections.
- Home page actions already route users into `/scan`.

## 3. Risks before implementing camera/upload flow

Technical risks:

- `sessionStorage` is browser-only, so the result flow will need a client boundary before reading the temporary image.
- The current scan action flow assumes navigation is always allowed and will need state-aware enable or validation logic.
- Camera lifecycle is not implemented yet, so permission handling, stream cleanup, capture logic, and error messaging all need to be defined carefully.
- The current scan type model does not yet represent permission state, camera readiness, image source, or temporary preview data.

Browser and device risks:

- `getUserMedia` requires a secure context in production.
- `facingMode: "environment"` is not guaranteed on every device or browser, so fallback handling is needed.
- If media tracks are not stopped correctly, the camera can remain active after retake or route changes.
- Large image data URLs may exceed `sessionStorage` limits on mobile devices.
- Invalid uploads or very large files need explicit validation and friendly error messages.

Project risks:

- There is a documentation path mismatch: the repo uses `docs/prdfrontend.md`, while some prior references mentioned `frontend/prdfrontend.md`.
- The current frontend already contains empty placeholder files for Sprint 04, which is useful, but they still require concrete design decisions before coding begins.

## 4. Questions before coding

- Should Sprint 04 only update `/scan` and `/result`, or should the home page preview area also become a real live camera preview now?
- Should `Analyze Material` stay hidden or disabled until an image exists, or should it remain visible and show an inline error when tapped without an image?
- Should captured or uploaded images be resized before storing them in `sessionStorage`, or should raw data URLs be used for this sprint?
- When camera permission is denied, should the primary fallback be upload-only, or should the UI also provide a retry path and browser guidance?
- Should Sprint 04 also begin saving lightweight recent scan history, or is history still intentionally deferred?

## 5. Recommendation: manual implementation, Codex implementation, or hybrid

Recommendation: hybrid.

Reasoning:

- The codebase is already structured well enough for Codex to implement the technical pieces inside the allowed Sprint 04 files.
- The remaining uncertainty is mostly product behavior, especially around upload fallback, disabled states, image resizing, and history scope.
- A hybrid approach is the safest path: confirm the few open UX decisions first, then let Codex implement the scoped camera and upload flow incrementally.
