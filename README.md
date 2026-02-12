# Convertin ✨

**Convertin** adalah web converter "all-in-one" premium berbasis **Python Flask**, **Redis**, dan **Celery**. Didesain untuk kecepatan, kebersihan sistem, dan kemudahan penggunaan.

---

## 📸 Preview
![Main Dashboard Placeholder](https://via.placeholder.com/800x450?text=Screenshot+Main+Dashboard)
*Tampilan utama dashboard Convertin dengan tema Glassmorphism.*

---

## 🌟 Fitur Utama
- **Smart Compression Analyzer**: Analisis metadata (bitrate, resolusi, durasi) & estimasi hasil konversi secara real-time.
- **Batch Processing**: Unggah dan konversi banyak file sekaligus secara multitasking.
- **Queue System**: Berbasis Redis & Celery, proses berjalan di background tanpa menghambat penggunaan web.
- **Auto Cleanup**: Folder `uploads` dan `outputs` otomatis dihapus "sampai bersih" setelah proses selesai.
- **Dukungan Format Luas**: Gambar, Audio, Video, Dokumen, dan Data.

---

## 🚀 Instalasi Cepat

1. **Persiapan:**
   - Install **Python 3.11+**, **FFmpeg**, dan **Redis Server**.

2. **Setup Project:**
   ```bash
   git clone https://github.com/Gansputra/convertin.git
   cd Convertin
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # atau
   .\venv\Scripts\activate   # Windows
   pip install -r requirements.txt
   ```

3. **Cara Menjalankan:**
   - **Terminal 1 (Worker):**
     ```bash
     celery -A celery_worker.celery worker --loglevel=info -P eventlet
     ```
   - **Terminal 2 (App):**
     ```bash
     python app.py
     ```
   - Buka: `http://127.0.0.1:5000`

---

## ⚙️ Edit Tools & Smart Analyzer
![Edit Tools Placeholder](https://via.placeholder.com/800x300?text=Screenshot+Edit+Tools+Analyzer)
*Fitur editing (resolusi, trim, scaling) yang sinkron dengan estimasi penghematan ukuran file.*

---

## 📁 Struktur Proyek
- `app.py`: Main Flask & API Routes.
- `celery_worker.py`: Background tasks logic.
- `converters/`: Mesin konversi per jenis file.
- `logic/`: Smart engine (Recommendation & Estimation).
- `templates/`: Antarmuka modern (Tailwind + Lucide).

---

## 👨‍💻 Author
**Gansputra**
- [GitHub](https://github.com/Gansputra/) | [Instagram](https://instagram.com/gans.putra_)

---
*Convert with speed, keep it clean.*
