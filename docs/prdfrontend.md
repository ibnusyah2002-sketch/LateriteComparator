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