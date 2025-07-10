# 📊 Evaluasi Platform Kursus Online dengan SMART dan SPI

Aplikasi web berbasis **Streamlit** untuk membantu dalam **pengambilan keputusan multikriteria (MCDM)** guna memilih platform kursus online terbaik. Aplikasi ini menggunakan dua metode populer:

- ✅ **SMART** (Simple Multi-Attribute Rating Technique)
- ⚙️ **SPI** (Simple Performance Index)

---

## 🚀 Fitur Aplikasi

- Input data platform secara **manual** atau **upload file CSV**
- Perhitungan skor berdasarkan kriteria:
  - Harga per bulan (cost)
  - Jumlah kursus (benefit)
  - Kualitas pengajar (benefit)
  - Sertifikat (benefit)
  - Kemudahan akses (benefit)
- Perbandingan dan perankingan dengan metode SMART & SPI
- Antarmuka sederhana dan interaktif

---

## 📁 Contoh Struktur CSV

File CSV yang bisa kamu upload harus memiliki kolom berikut:

```csv
Platform,Harga_per_Bulan,Jumlah_Kursus,Kualitas_Pengajar,Sertifikat,Kemudahan_Akses
Coursera,450000,6000,90,1,95
Udemy,250000,210000,85,1,90
