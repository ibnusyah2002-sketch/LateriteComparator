# LCGC Database Schema

## Project

LCGC — Laterite Comparator for Grade Control

Application name:

Laterite Comparator

Tagline:

Scan. Compare. Identify.

---

## Database Purpose

The database stores comparator sample metadata, QAQC assay data, material descriptions, and image references.

The database supports the main product principle:

LCGC is an AI Comparator, not an AI classifier.

The system compares a scanned material image against stored comparator samples and returns the most visually similar samples.

Correct wording:

```text
This scanned material is visually similar to comparator sample BG1 - 01.
```

Avoid:

```text
This material is definitely Earthy Saprolite.
```

---

## Source Data

Main local source:

```text
database/QAQC.xlsx
```

Important rules:

- `database/*` is ignored from Git.
- The Excel database must not be committed.
- The Excel file is used as the local source for database import.
- The Excel file contains QAQC, material description, and documentation reference data.

---

## Source Image Dataset

Main local image source:

```text
dataset/
```

Example current image folder:

```text
D:\Komparator\LateriteComparator\dataset\BG1 - 01\
├── raw.jpg
└── scale.jpg
```

Important rules:

- `dataset/*` is ignored from Git.
- Dataset images must not be committed.
- Each image folder name must match the `Code` value in the Excel QAQC database.
- Each sample folder should contain at least `raw.jpg`.
- `scale.jpg` is strongly recommended because it contains scale/reference measurement.

---

## Image Folder Naming Rule

Each comparator image folder name must match the `Code` value from the Excel QAQC database.

Example Excel row:

```text
Code = BG1 - 01
```

Expected local image folder:

```text
dataset/BG1 - 01/
├── raw.jpg
└── scale.jpg
```

This rule allows the import script to automatically connect QAQC data with comparator images.

Folder naming formula:

```text
dataset/{Code}/raw.jpg
dataset/{Code}/scale.jpg
```

Example:

```text
Code: BG1 - 01
Raw image: dataset/BG1 - 01/raw.jpg
Scale image: dataset/BG1 - 01/scale.jpg
```

Important:

- Keep the original `Code` value in the database.
- Folder name should match the Excel `Code` exactly.
- Use `raw.jpg` for the original material photo.
- Use `scale.jpg` for the material photo with scale/reference ruler.
- Do not commit dataset images to Git.

---

## Source Excel Columns

Expected columns from `database/QAQC.xlsx`:

```text
NO
Code
Tanggal Sample
Kode Sample
INCR
Ni
Co
Fe
SiO2
CaO
MgO
Cr2O3
AL2O3
Cr
Fe/Ni
S/M
BC
Warna
Zona
Ukuran
Komposisi
Keterangan
Dokumentasi (RAW)
Dokumentasi (SI GC)
PPT
Front
```

---

## Main Database Entities

The MVP database uses two main tables:

```text
comparator_samples
comparator_images
```

### 1. comparator_samples

This table stores one row per comparator sample.

It represents the Excel QAQC row.

Primary human lookup key:

```text
code
```

Example:

```text
BG1 - 01
```

### 2. comparator_images

This table stores image references for each comparator sample.

One sample can have multiple images.

Example:

```text
BG1 - 01
├── raw.jpg
└── scale.jpg
```

Therefore, one sample in `comparator_samples` can have multiple rows in `comparator_images`.

---

## Relationship Model

Relationship:

```text
comparator_samples.id
↓
comparator_images.sample_id
```

Human-readable relationship:

```text
comparator_samples.code = comparator_images.code
```

Example:

### comparator_samples

| id | code | ni | fe | zone | color |
|---|---|---:|---:|---|---|
| uuid-001 | BG1 - 01 | 1.82 | 23.41 | Earthy Saprolite | Brown Greenish |

### comparator_images

| id | sample_id | code | image_type | local_path |
|---|---|---|---|---|
| uuid-img-001 | uuid-001 | BG1 - 01 | raw | dataset/BG1 - 01/raw.jpg |
| uuid-img-002 | uuid-001 | BG1 - 01 | scale | dataset/BG1 - 01/scale.jpg |

---

## Field Mapping: Excel to comparator_samples

| Excel Column | Database Field | Type | Notes |
|---|---|---|---|
| NO | source_no | integer | Original row number |
| Code | code | text | Unique comparator sample code |
| Tanggal Sample | sample_date | date | Sampling date |
| Kode Sample | sample_code | text | Original sample code |
| INCR | incr | text | Increment information |
| Ni | ni | numeric | QAQC assay |
| Co | co | numeric | QAQC assay |
| Fe | fe | numeric | QAQC assay |
| SiO2 | sio2 | numeric | QAQC assay |
| CaO | cao | numeric | QAQC assay |
| MgO | mgo | numeric | QAQC assay |
| Cr2O3 | cr2o3 | numeric | QAQC assay |
| AL2O3 | al2o3 | numeric | QAQC assay |
| Cr | cr | numeric | QAQC assay |
| Fe/Ni | fe_ni | numeric | Ratio |
| S/M | s_m | numeric | Ratio |
| BC | bc | text | BC classification/value |
| Warna | color | text | Material color |
| Zona | zone | text | Laterite zone |
| Ukuran | size_text | text | Material size |
| Komposisi | composition | text | Material composition |
| Keterangan | description | text | Material description |
| Dokumentasi (RAW) | documentation_raw | text | Raw documentation reference |
| Dokumentasi (SI GC) | documentation_si_gc | text | Grade control documentation reference |
| PPT | ppt_reference | text | PPT reference |
| Front | front_reference | text | Front image/reference |

---

## Field Mapping: Image Dataset to comparator_images

| Source | Database Field | Example |
|---|---|---|
| Excel `Code` | code | BG1 - 01 |
| Matching sample row | sample_id | uuid from comparator_samples |
| `dataset/{Code}/raw.jpg` | local_path | dataset/BG1 - 01/raw.jpg |
| raw filename | image_type | raw |
| `dataset/{Code}/scale.jpg` | local_path | dataset/BG1 - 01/scale.jpg |
| scale filename | image_type | scale |
| Supabase Storage path later | storage_path | comparator-images/bg1-01/raw.jpg |
| Supabase public URL later | public_url | URL from Supabase Storage |
| Primary comparator image | is_primary | true for raw image |

---

## Image Strategy

Images should not be stored directly inside Git.

Current local image structure:

```text
dataset/
├── BG1 - 01/
│   ├── raw.jpg
│   └── scale.jpg
├── BG1 - 02/
│   ├── raw.jpg
│   └── scale.jpg
```

Folder naming rule:

```text
dataset/{Code}/raw.jpg
dataset/{Code}/scale.jpg
```

Image type meaning:

- `raw`: original material photo
- `scale`: material photo with scale/reference ruler
- `other`: optional extra image type for future needs

MVP rule:

- `raw.jpg` is the primary comparator image.
- `scale.jpg` is a supporting visual reference.
- If `scale.jpg` is missing, the sample can still be used.
- If `raw.jpg` is missing, the sample should be flagged for review.

---

## Future Supabase Storage Structure

Recommended future Supabase Storage bucket:

```text
comparator-images
```

Recommended storage path:

```text
comparator-images/bg1-01/raw.jpg
comparator-images/bg1-01/scale.jpg
comparator-images/bg1-02/raw.jpg
comparator-images/bg1-02/scale.jpg
```

Important:

- Keep original sample code in database, for example `BG1 - 01`.
- Use normalized folder keys for storage path, for example `bg1-01`.
- The normalized path is only for storage safety and URL consistency.
- The original code remains the main human-readable reference.

---

## Code Normalization Rule for Storage Path

Original code:

```text
BG1 - 01
```

Normalized storage key:

```text
bg1-01
```

Recommended normalization rule:

```text
1. trim whitespace
2. convert to lowercase
3. replace spaces with hyphen
4. remove duplicate hyphens
5. keep letters and numbers
```

Examples:

| Original Code | Normalized Storage Key |
|---|---|
| BG1 - 01 | bg1-01 |
| BG1 - 02 | bg1-02 |
| RB4-015 | rb4-015 |

Important:

The database field `code` should still store the original value.

---

## Table: comparator_samples

Purpose:

Stores QAQC and material description data from Excel.

Recommended fields:

| Field | Type | Required | Description |
|---|---|---|---|
| id | uuid | yes | Primary key |
| source_no | integer | no | Original Excel row number |
| code | text | yes | Unique comparator code |
| sample_date | date | no | Sample date |
| sample_code | text | no | Original sample code |
| incr | text | no | Increment information |
| ni | numeric | no | Nickel grade |
| co | numeric | no | Cobalt grade |
| fe | numeric | no | Iron grade |
| sio2 | numeric | no | Silica |
| cao | numeric | no | Calcium oxide |
| mgo | numeric | no | Magnesium oxide |
| cr2o3 | numeric | no | Chromium oxide |
| al2o3 | numeric | no | Aluminum oxide |
| cr | numeric | no | Chromium |
| fe_ni | numeric | no | Fe/Ni ratio |
| s_m | numeric | no | S/M ratio |
| bc | text | no | BC classification/value |
| color | text | no | Material color |
| zone | text | no | Laterite zone |
| size_text | text | no | Material size |
| composition | text | no | Material composition |
| description | text | no | Material description |
| documentation_raw | text | no | Raw documentation reference |
| documentation_si_gc | text | no | Grade control documentation reference |
| ppt_reference | text | no | PPT reference |
| front_reference | text | no | Front reference |
| status | text | yes | active/inactive/review |
| created_at | timestamptz | yes | Created timestamp |
| updated_at | timestamptz | yes | Updated timestamp |

---

## Table: comparator_images

Purpose:

Stores image references for each comparator sample.

A sample may have multiple image rows.

Current expected image types:

```text
raw
scale
other
```

Example:

| code | image_type | local_path |
|---|---|---|
| BG1 - 01 | raw | dataset/BG1 - 01/raw.jpg |
| BG1 - 01 | scale | dataset/BG1 - 01/scale.jpg |

Recommended fields:

| Field | Type | Required | Description |
|---|---|---|---|
| id | uuid | yes | Primary key |
| sample_id | uuid | yes | Foreign key to comparator_samples.id |
| code | text | yes | Human-readable sample code |
| image_type | text | yes | raw, scale, or other |
| local_path | text | no | Local dataset path |
| storage_path | text | no | Supabase Storage path |
| public_url | text | no | Supabase image URL |
| is_primary | boolean | yes | true for primary comparator image |
| embedding | vector(512) | no | Future OpenCLIP image embedding |
| metadata | jsonb | yes | Extra image metadata |
| created_at | timestamptz | yes | Created timestamp |

MVP image rule:

- `raw` image should have `is_primary = true`.
- `scale` image should have `is_primary = false`.

---

## Table: scan_sessions

Purpose:

Stores future scan activity and result snapshots.

This table is optional for early MVP but useful for future history, analytics, and validation.

Recommended fields:

| Field | Type | Required | Description |
|---|---|---|---|
| id | uuid | yes | Primary key |
| input_image_path | text | no | Uploaded user image path |
| input_image_source | text | no | camera/upload |
| best_match_sample_id | uuid | no | Best matched sample |
| best_match_code | text | no | Best matched sample code |
| similarity_score | numeric | no | Similarity score |
| confidence_label | text | no | Very High, High, Medium, Low |
| result_payload | jsonb | yes | Full result snapshot |
| created_at | timestamptz | yes | Created timestamp |

---

## MVP Required Tables

Required for MVP:

```text
1. comparator_samples
2. comparator_images
```

Optional but recommended later:

```text
3. scan_sessions
4. user_feedback
5. validation_logs
```

---

## Import Strategy

The import process should happen in stages.

### Stage 1 — Validate Excel Columns

Read:

```text
database/QAQC.xlsx
```

Check that required columns exist:

```text
Code
Ni
Co
Fe
SiO2
MgO
Warna
Zona
Ukuran
Komposisi
Keterangan
```

Output:

```text
Excel column validation report
```

### Stage 2 — Validate Image Folders

For each Excel row:

```text
code = row["Code"]
```

Check:

```text
dataset/{code}/raw.jpg
dataset/{code}/scale.jpg
```

Validation rules:

- Missing `raw.jpg` = warning or review required
- Missing `scale.jpg` = warning only
- Folder missing = review required
- Extra files = allowed but should be reported

### Stage 3 — Create Import Preview

Generate local preview data:

```text
backend/data_preview/comparator_samples_preview.json
backend/data_preview/comparator_images_preview.json
```

These preview files should not include image bytes.

They should only include metadata and paths.

Example sample preview:

```json
{
  "code": "BG1 - 01",
  "ni": 1.82,
  "fe": 23.41,
  "zone": "Earthy Saprolite",
  "color": "Brown Greenish"
}
```

Example image preview:

```json
{
  "code": "BG1 - 01",
  "image_type": "raw",
  "local_path": "dataset/BG1 - 01/raw.jpg",
  "is_primary": true
}
```

### Stage 4 — Supabase Import

Later, insert data into:

```text
comparator_samples
comparator_images
```

Upload images into Supabase Storage only after validation is clean.

---

## Validation Checklist

Before importing to Supabase:

| Check | Expected Result |
|---|---|
| Excel file exists | `database/QAQC.xlsx` found |
| Dataset folder exists | `dataset/` found |
| Code column exists | Yes |
| Code values are unique | Yes |
| Empty Code values | None |
| Required assay columns exist | Yes |
| Required description columns exist | Yes |
| Each Code has matching folder | Preferably yes |
| Each folder has raw.jpg | Required for comparator |
| Each folder has scale.jpg | Recommended |
| database folder ignored by Git | Yes |
| dataset folder ignored by Git | Yes |

---

## AI Search Plan

This is for future sprint, not Sprint 06.

Future flow:

```text
User captures/uploads material image
↓
Backend receives image
↓
Image preprocessing with OpenCV
↓
Image embedding generated with OpenCLIP
↓
Vector similarity search against comparator_images.embedding
↓
Best visual matches returned
↓
Frontend displays user image vs comparator image
```

Important:

The AI should compare visual similarity, not make an absolute classification.

Correct wording:

```text
This scanned material is visually similar to comparator sample BG1 - 01.
```

Avoid:

```text
This material is definitely BG1 - 01.
This material is definitely Earthy Saprolite.
```

---

## Result Payload Principle

Frontend result should receive structured data like:

```json
{
  "best_match": {
    "code": "BG1 - 01",
    "similarity": 98.7,
    "confidence": "Very High",
    "zone": "Earthy Saprolite",
    "color": "Brown Greenish"
  },
  "qaqc": {
    "ni": 1.82,
    "co": 0.08,
    "fe": 23.41,
    "mgo": 9.62,
    "sio2": 41.2
  },
  "description": [
    {
      "label": "Zona",
      "value": "Earthy Saprolite"
    },
    {
      "label": "Warna",
      "value": "Brown Greenish"
    },
    {
      "label": "Komposisi",
      "value": "Serpentine, Goethite, Garnierite traces"
    }
  ],
  "images": {
    "user_image_url": "temporary-upload-path",
    "comparator_raw_url": "comparator-images/bg1-01/raw.jpg",
    "comparator_scale_url": "comparator-images/bg1-01/scale.jpg"
  },
  "alternative_matches": [
    {
      "code": "BG1 - 02",
      "similarity": 95.4
    },
    {
      "code": "BG1 - 03",
      "similarity": 93.8
    }
  ]
}
```

---

## Security and Git Rules

Do not commit:

```text
database/*
dataset/*
.env
.env.local
node_modules
.next
```

Safe to commit:

```text
docs/database_schema.md
docs/supabase_schema.sql
scripts/*
backend/*
frontend/*
```

Data privacy rule:

- Excel QAQC stays local during development.
- Dataset images stay local during development.
- Public repository should only contain schema, scripts, and non-sensitive examples.

---

## Current Sprint Status

Sprint 06 focus:

```text
Database preparation
Excel mapping
Image folder mapping
Schema planning
Validation before Supabase import
```

Not included in Sprint 06 yet:

```text
AI model
OpenCLIP embedding
Supabase Storage upload
Production deployment
Authentication
```

Next expected sprint:

```text
Sprint 06C — Excel and image folder validation script
```