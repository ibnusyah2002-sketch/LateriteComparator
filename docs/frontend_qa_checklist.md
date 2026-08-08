# Frontend QA Checklist - Sprint 05

## Project

LCGC — Laterite Comparator for Grade Control

## Product Principle

LCGC is an AI Comparator, not an AI classifier.

Correct wording:
- "This scanned material is visually similar to comparator sample RB4-015."
- "Visual Match Found"
- "Comparator Result"

Avoid:
- "This material is definitely..."
- "AI classification result"
- "Detected material is..."

---

## Route Checklist

| Route | Expected Result | Status |
|---|---|---|
| / | Scanner homepage opens | Pass |
| /analysis | Redirects to / if no scan image exists | Pass |
| /result | Shows empty state if no scan image exists | Pass |
| /scan | Redirects to / | Pass |
| /history | History page opens | Pass |
| /settings | Settings page opens | Pass |

---

## Homepage Scanner Checklist

| Test | Expected Result | Status |
|---|---|---|
| Open homepage | Scanner frame appears | Pending |
| Camera inactive state | Capture Material is visible but disabled | Pending |
| Camera inactive state | Enable button appears at top-right of camera frame | Pending |
| Click Enable | Browser requests camera permission | Pending |
| Allow permission | Live camera preview appears | Pending |
| Live camera state | Enable button changes to Stop | Pending |
| Click Stop | Camera preview stops | Pending |
| Camera active state | Capture Material becomes active | Pending |
| Click Capture Material | Captured image preview appears | Pending |
| After capture | Analyze Material button appears | Pending |
| After capture | Retake and Change buttons appear | Pending |
| Click Retake | Camera starts again and preview resets | Pending |
| Click Upload Image | File picker opens | Pending |
| Upload valid image | Uploaded preview appears | Pending |
| Upload invalid file | Friendly error appears | Pending |

---

## Analysis Flow Checklist

| Test | Expected Result | Status |
|---|---|---|
| Click Analyze Material | Navigates to /analysis | Pending |
| /analysis opens | Loading UI appears | Pending |
| Analysis stages | Stages progress visually | Pending |
| After loading | Automatically navigates to /result | Pending |
| No image in sessionStorage | /analysis redirects to / | Pending |

---

## Result Page Checklist

| Test | Expected Result | Status |
|---|---|---|
| Result after capture | User Photo appears | Pending |
| Result after upload | User Photo appears | Pending |
| Comparator section | Shows RB4-015 placeholder | Pending |
| Similarity section | Shows 98.7% and Very High | Pending |
| QAQC cards | Ni, Co, Fe, MgO, SiO2 appear | Pending |
| Dynamic description | Description cards appear | Pending |
| Alternative matches | Alternative match cards appear | Pending |
| Click Scan Again | Returns to homepage | Pending |
| Open /result without scan | Empty state appears | Pending |

---

## Navigation Checklist

| Test | Expected Result | Status |
|---|---|---|
| Bottom nav Scanner | Goes to / | Pending |
| Bottom nav History | Goes to /history | Pending |
| Bottom nav Settings | Goes to /settings | Pending |
| Scanner nav active | Active on /, /analysis, /result | Pending |
| No /scan nav confusion | /scan is not exposed as main navigation | Pending |

---

## Mobile Layout Checklist

| Device Width | Expected Result | Status |
|---|---|---|
| 390px | Layout fits mobile screen | Pending |
| 412px | Layout fits mobile screen | Pending |
| 430px | Layout fits mobile screen | Pending |
| Desktop | Mobile frame remains centered | Pending |

---

## Build Checklist

| Command | Expected Result | Status |
|---|---|---|
| npm run dev | Runs without terminal error | Pass |
| npm run build | Build completes successfully | Pass |

---

## Notes

Bugs found:

- None yet

Polish needed:

- None yet