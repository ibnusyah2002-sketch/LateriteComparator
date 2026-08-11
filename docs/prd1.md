PRD kita letakkan di:

```text
docs/prd.md
```

Struktur yang benar:

```text
LateriteComparator/
├── AGENTS.md
├── docs/
│   ├── prd.md
│   ├── design_system.md
│   ├── architecture.md
│   ├── agent.md
│   ├── database.md
│   └── ai_engine.md
├── frontend/
├── backend/
├── ai/
└── ...
```

Jadi:

```text
AGENTS.md              → aturan untuk Cursor/AI coding agent
docs/prd.md            → dokumen kebutuhan produk
docs/design_system.md  → aturan tampilan/UI
docs/architecture.md   → arsitektur teknis
```

Berikut PRD yang pernah kita buat, saya rapikan menjadi versi yang siap Anda simpan sebagai `docs/prd.md`.

---

````markdown
# LCGC PRD v1.0

## Product Name

LCGC

## Full Name

Laterite Comparator for Grade Control

## Application Name

Laterite Comparator

## Tagline

Scan. Compare. Identify.

---

# 1. Product Vision

LCGC adalah aplikasi web berbasis AI Comparator untuk membantu proses identifikasi material nikel laterit pada aktivitas Grade Control.

Aplikasi ini memungkinkan pengguna mengambil atau mengunggah foto material laterit, lalu sistem akan membandingkan foto tersebut dengan database komparator yang telah tervalidasi.

LCGC tidak bertujuan menggantikan keputusan geologist atau engineer. LCGC berfungsi sebagai alat bantu untuk meningkatkan konsistensi, efisiensi, dan kecepatan deskripsi material di lapangan.

Nickel laterite comparator samples are organized by geological zones:
topsoil, limonite, saprolite, and bedrock/fresh rock.

Limonite can be subdivided into red limonite and yellow limonite.
Saprolite can be subdivided into earthy saprolite and rocky saprolite.

Each comparator sample represents a known field appearance and has associated lab assay data.
Multiple samples can belong to the same zone when they show different visual appearances.
The system should compare scanned material to comparator samples, not directly classify the material as a definitive zone or grade.
---

# 2. Core Principle

LCGC is not an AI classification system.

LCGC is an AI Comparator system.

Prinsip utama:

User Image  
→ Visual Analysis  
→ Similarity Search  
→ Comparator Result  
→ QAQC Data  
→ Material Description

Aplikasi tidak boleh menyatakan bahwa material hasil scan adalah material tertentu secara absolut.

Kalimat yang benar:

> Material yang Anda scan memiliki kemiripan visual 98.7% dengan sampel komparator RB4-015.

Kalimat yang harus dihindari:

> Material ini pasti RB4-015.

---

# 3. Problem Statement

Saat ini proses identifikasi material laterit masih memiliki beberapa kendala:

- Deskripsi material sangat bergantung pada pengalaman individu.
- Interpretasi antar operator atau engineer dapat berbeda.
- Database komparator masih berbentuk manual atau semi-digital.
- Pencarian sampel pembanding membutuhkan waktu.
- Tidak ada sistem visual yang membantu membandingkan foto material dengan database.
- Tidak ada riwayat digital hasil scan.
- Pembelajaran material laterit untuk personel baru masih belum interaktif.

---

# 4. Solution

LCGC menyediakan aplikasi web yang dapat dibuka melalui browser HP.

Pengguna cukup:

1. Membuka aplikasi.
2. Kamera langsung aktif.
3. Mengambil gambar material.
4. Sistem menganalisis gambar.
5. Sistem mencari material paling mirip dari database komparator.
6. Aplikasi menampilkan hasil berupa:
   - Similarity score
   - Foto user
   - Foto komparator
   - Kode sample
   - Zona
   - Warna
   - Ukuran
   - Komposisi
   - Keterangan
   - Data QAQC
   - Alternative matches

---

# 5. Target Users

## Primary User

- Grade Control Engineer
- Grade Control Operator

## Secondary Users

- Geologist
- Mining Engineer
- QAQC Team
- Supervisor
- Mahasiswa
- Visitor tambang
- Management

---

# 6. MVP Objective

Dalam versi MVP, aplikasi harus bisa menjalankan alur utama berikut:

Open App  
→ Camera / Upload Image  
→ Analyze Material  
→ Show Loading  
→ Show Best Comparator Match  
→ Show QAQC Data  
→ Show Description  
→ Show Alternative Matches  
→ Save Recent Scan

---

# 7. MVP Success Criteria

Aplikasi dianggap berhasil untuk MVP jika:

- Bisa dibuka melalui browser HP.
- Halaman pertama langsung menampilkan UI scan.
- User bisa mengambil atau mengunggah gambar.
- Sistem dapat menampilkan hasil dummy terlebih dahulu.
- Sistem memiliki halaman result dengan struktur final.
- Result page menampilkan foto user dan foto komparator berdampingan.
- Result page menampilkan similarity score.
- Result page menampilkan QAQC card.
- Result page menampilkan dynamic description.
- Result page menampilkan alternative matches.
- History scan dapat ditampilkan.
- Struktur aplikasi siap dihubungkan ke backend dan AI Engine.

---

# 8. Main Product Modules

## 8.1 Laterite Vision

Modul untuk user lapangan.

Fitur:

- Camera preview
- Capture material
- Upload image
- Loading analysis
- Result view
- Recent scan
- Scan again

---

## 8.2 Comparator Studio

Modul admin untuk pengelolaan database.

Fitur fase awal:

- View comparator database
- Import Excel
- Upload image
- Edit sample
- Delete sample
- Manage image folder

Fitur ini tidak menjadi prioritas utama MVP awal, tetapi disiapkan dalam roadmap.

---

## 8.3 Comparator Engine

Modul AI dan backend.

Fungsi:

- Image upload
- Image preprocessing
- Image quality check
- OpenCV feature extraction
- OpenCLIP embedding
- pgvector similarity search
- Return Top 5 comparator matches
- Return QAQC and material description

---

# 9. User Flow

## Main Flow

1. User membuka aplikasi.
2. Kamera atau scan interface muncul.
3. User mengambil foto material.
4. Sistem menampilkan loading analysis.
5. Sistem mencari material paling mirip.
6. Sistem menampilkan halaman result.
7. User dapat scan ulang atau melihat alternative matches.

Flow:

Open App  
→ Home / Scan Interface  
→ Capture / Upload  
→ Processing  
→ Result  
→ Scan Again / History

---

# 10. Required Routes

Frontend routes:

- `/`
- `/scan`
- `/result`
- `/history`
- `/settings`
- `/admin` later

---

# 11. Screen Requirements

## 11.1 Home Screen

Homepage harus langsung mengarahkan user ke fungsi utama.

Elemen:

- Logo LCGC
- Laterite Comparator
- Grade Control
- Tagline: Scan. Compare. Identify.
- Camera preview placeholder
- Capture Material button
- Upload Image button
- Recent Scan section
- Bottom navigation

Prioritas:

1. Camera
2. Capture
3. Upload
4. Recent scan

---

## 11.2 Scan Screen

Elemen:

- Camera preview
- Scanner frame
- Instruction text
- Capture button
- Upload image option
- Retake option later

Instruction text:

> Position the laterite material inside the frame.

---

## 11.3 Loading Screen

Loading harus memberi kesan AI sedang bekerja.

Tahapan:

- Detecting Material
- Extracting Visual Features
- Finding Comparator
- Generating Result

---

## 11.4 Result Screen

Urutan tampilan result:

1. Similarity score
2. Confidence label
3. User photo vs comparator photo
4. Material summary
5. QAQC cards
6. Dynamic description cards
7. Alternative matches
8. Scan Again button

---

## 11.5 History Screen

Menampilkan riwayat scan.

MVP:

- 3 recent scans
- Thumbnail
- Material code
- Similarity
- Date

---

## 11.6 Settings Screen

MVP placeholder:

- App name
- Version
- Theme
- Data source
- About LCGC

---

# 12. Result Page Data Display

## Similarity

Contoh:

- 98.7%
- Very High Confidence

Confidence rules sementara:

- 90–100% = Very High
- 80–89% = High
- 70–79% = Medium
- Below 70% = Low

---

## Image Comparison

Result page wajib menampilkan:

- User photo
- Comparator photo

Kedua foto harus tampil berdampingan atau stacked secara mobile-friendly.

Prinsip:

> Everything starts from comparison.

---

## QAQC Cards

Data QAQC ditampilkan dalam bentuk card, bukan tabel panjang.

Field utama:

- Ni
- Co
- Fe
- SiO2
- CaO
- MgO
- Cr2O3
- Al2O3
- Cr
- Fe/Ni
- S/M
- BC

---

## Dynamic Description

Deskripsi tidak boleh di-hardcode berdasarkan urutan tetap frontend.

Backend idealnya mengirim format:

```json
{
  "attributes": [
    { "label": "Zona", "value": "Saprolite" },
    { "label": "Warna", "value": "Brown Greenish" },
    { "label": "Ukuran", "value": "Gravel" },
    { "label": "Komposisi", "value": "Serpentine, Goethite" },
    { "label": "Keterangan", "value": "Material with greenish brown tone and earthy texture." }
  ]
}
````

Frontend hanya membaca dan menampilkan daftar attributes tersebut.

---

# 13. Comparator Database Fields

Database Excel yang tersedia memiliki kolom:

* NO
* Code
* Tanggal Sample
* Kode Sample
* INCR
* Ni
* Co
* Fe
* SiO2
* CaO
* MgO
* Cr2O3
* AL2O3
* Cr
* Fe/Ni
* S/M
* BC
* Warna
* Zona
* Ukuran
* Komposisi
* Keterangan
* Dokumentasi (RAW)
* Dokumentasi (SI GC)
* PPT
* Front

Kolom utama untuk AI Comparator:

* Code
* Warna
* Zona
* Ukuran
* Komposisi
* Keterangan
* Front
* Ni
* Fe
* MgO
* SiO2

---

# 14. Dataset Image Structure

Struktur folder gambar:

```text
dataset/
└── images/
    ├── rb4-001/
    │   └── front.jpg
    ├── rb4-002/
    │   └── front.jpg
    └── rb4-003/
        └── front.jpg
```

Excel boleh menggunakan Code uppercase:

```text
RB4-001
```

File/folder image sebaiknya lowercase:

```text
rb4-001/front.jpg
```

Aplikasi dapat mengubah Code menjadi lowercase saat mencari gambar.

---

# 15. AI Pipeline

MVP AI pipeline:

Image Upload
→ Image Quality Check
→ OpenCV Preprocessing
→ OpenCLIP Embedding
→ pgvector Similarity Search
→ Top 5 Matches
→ Load Comparator Data
→ Return Result JSON

---

# 16. AI Output

AI tidak menghasilkan deskripsi baru dari nol.

AI mencari sampel paling mirip dari database, lalu mengambil deskripsi dari database.

Output:

* Best match
* Similarity score
* Comparator image
* QAQC data
* Dynamic attributes
* Alternative matches

---

# 17. Technology Stack

## Frontend

* Next.js App Router
* React
* TypeScript
* Tailwind CSS
* Lucide Icons

## Backend

* FastAPI
* Python

## Database

* Supabase PostgreSQL
* pgvector
* Supabase Storage

## AI

* OpenCV
* OpenCLIP
* Image embeddings
* Visual similarity search

## Deployment

* Vercel for frontend
* Railway for backend
* Supabase for database and storage

---

# 18. Design Direction

Design style:

* Dark industrial
* Mobile first
* Premium
* Scientific
* Field-friendly
* Minimal text
* Large touch targets
* High contrast

Color direction:

* Black background
* Dark card
* Green accent
* White text
* Gray secondary text

Refer to:

```text
docs/design_system.md
```

---

# 19. Non-Goals for MVP

Hal berikut tidak dikerjakan dulu pada MVP awal:

* Fine-tuning model
* Admin dashboard lengkap
* User role lengkap
* Offline mode
* PDF report
* Automatic retraining
* Supervisor feedback loop
* Advanced analytics
* Enterprise security
* Multi-company system

---

# 20. V2 Roadmap

Setelah MVP:

* Supabase integration
* Real database import
* Real image upload
* OpenCLIP similarity search
* Admin dashboard
* Dataset management
* Supervisor validation
* Fine-tuning
* Analytics dashboard
* PDF report
* Offline mode

---

# 21. Product Positioning

LCGC bukan sekadar aplikasi komparator.

LCGC adalah fondasi platform visual intelligence untuk identifikasi material laterit pada aktivitas Grade Control.

Positioning statement:

> LCGC helps grade control teams compare field material photos with validated laterite comparator samples using AI-powered visual similarity search.

---

# 22. Demo Goal

Untuk hackathon, demo utama harus memperlihatkan:

1. User membuka aplikasi.
2. User melakukan scan atau upload foto.
3. Loading analysis berjalan.
4. Result page muncul.
5. Foto user dibandingkan dengan foto komparator.
6. Similarity score tampil.
7. QAQC data tampil.
8. Alternative matches tampil.

Demo harus membuat juri langsung memahami:

> Aplikasi ini tidak menebak material, tetapi membandingkan foto user dengan database komparator yang tervalidasi.

````

---

## Step Anda sekarang

Buat file:

```text
docs/prd.md
````

Lalu salin isi PRD di atas.

Setelah selesai, simpan dengan:

```text
Ctrl + S
```

Setelah itu struktur dokumen Anda menjadi:

```text
docs/
├── prd.md
├── design_system.md
├── architecture.md
└── agent.md
```

Lalu tetap buat juga:

```text
AGENTS.md
```

di root project.
