# 🤖 Smart PDF Summarizer (Terminal AI Agent)

**Smart PDF Summarizer** adalah agen AI berbasis terminal (CLI) yang dirancang untuk membantu efisiensi manajemen dokumen. Alat ini dapat secara otomatis melacak keberadaan file PDF di laptop Anda dan menyajikan ringkasan poin-poin penting secara instan.

Proyek ini dibuat menggunakan Python murni dengan pendekatan *Rule-Based NLP* (tanpa API key berbayar).

---

## ✨ Fitur Unggulan

* **🔍 Smart Search System:** Tidak perlu memindahkan file ke folder script atau mengetik path panjang. AI otomatis memindai folder *Downloads*, *Documents*, dan *Desktop* untuk menemukan file yang Anda minta.
* **📝 Auto Summarizer:** Mengekstrak teks, membersihkan format yang berantakan, dan menganalisis 3 poin terpenting berdasarkan algoritma frekuensi kata kunci.
* **🎨 Interactive CLI:** Antarmuka terminal yang rapi dan berwarna (User Friendly) menggunakan library `colorama`.
* **🚀 Offline & Cepat:** Berjalan 100% lokal tanpa koneksi internet.

---

## 📸 Demo Preview

*(Tempelkan screenshot terminal Anda di sini, atau hapus baris ini jika belum ada gambar)*

> **Contoh Penggunaan:**
> User: "ringkas jurnal_skripsi.pdf"
> AI: (Mencari file...) -> (Menemukan di folder Downloads) -> (Menampilkan Ringkasan)

---

## 🛠️ Instalasi

Pastikan Anda sudah menginstall Python 3.x di komputer Anda.

1.  **Clone repositori ini**
    ```bash
    git clone [https://github.com/username-anda/smart-pdf-summarizer.git](https://github.com/username-anda/smart-pdf-summarizer.git)
    cd smart-pdf-summarizer
    ```

2.  **Install Library yang dibutuhkan**
    Hanya butuh dua library ringan:
    ```bash
    pip install PyPDF2 colorama
    ```

---

## 🚀 Cara Penggunaan

1.  Jalankan script utama:
    ```bash
    python pdf_agent.py
    ```

2.  Saat muncul prompt `User ➤`, ketik perintah dengan format:
    ```text
    ringkas [nama_file.pdf]
    ```

3.  **Contoh:**
    ```text
    User ➤ ringkas laporan_akhir.pdf
    ```
    *Catatan: Anda tidak perlu tahu di mana lokasi file tersebut, asalkan ada di folder umum (Documents/Downloads), AI akan menemukannya.*

---

## 🧠 Cara Kerja (Technical Logic)

1.  **Text Extraction:** Script menggunakan `PyPDF2` untuk mengambil raw text dari halaman PDF.
2.  **Preprocessing:** Membersihkan *noise* seperti spasi ganda dan *hyphenation* (kata terpotong di ujung baris).
3.  **Word Weighting:** Menghitung frekuensi kata (TF) untuk menentukan topik utama, dengan memfilter *stopwords* (kata sambung umum).
4.  **Sentence Scoring:** Memberi nilai pada setiap kalimat berdasarkan jumlah kata kunci yang dikandungnya.
5.  **Ranking:** Mengambil 3 kalimat dengan skor tertinggi sebagai ringkasan.

---

## 📂 Struktur Project
ai-agent-summarizer/ 
    │ 
    ├── pdf_agent.py # Main Script (AI Logic & Interface) 
    ├── README.md # Dokumentasi Project 
    └── requirements.txt # Daftar Library

**Author:** [Fathir Raihan Muhammad]
