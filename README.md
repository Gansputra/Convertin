# Convertin ✨ 
**Convertin** adalah aplikasi web pengonversi file "all-in-one" premium berbasis Python Flask. Kini dilengkapi dengan sistem antrian (Queue) profesional, Batch Processing, dan pratinjau file yang canggih untuk memberikan pengalaman pengguna yang mulus dan cepat.

## 🚀 Fitur Utama
- **Batch Processing**: Unggah dan konversi banyak file sekaligus tanpa menunggu satu per satu.
- **Queue System (Redis + Celery)**: Proses konversi berjalan di background. Anda tetap bisa menjelajahi situs selagi file diproses.
- **Real-time Progress Bar**: Pantau progres konversi setiap file secara langsung.
- **Advanced File Preview**: Pratinjau instan untuk Gambar, Video, dan Audio sebelum dikonversi.
- **Smart Recommendation**: Sistem otomatis menyarankan format terbaik berdasarkan metadata file Anda.
- **Batch Download (ZIP)**: Unduh semua hasil konversi dalam satu file arsip ZIP yang rapi.
- **Dukungan Format Luas**:
  - **Gambar**: JPG, JPEG, PNG, WEBP, SVG.
  - **Audio**: MP3, WAV, M4A, FLAC.
  - **Video**: MP4, MKV, GIF.
  - **Dokumen**: PDF, DOCX, DOC. (PDF <-> Word)
  - **Data**: CSV, JSON, XLSX.

## 🛠️ Persyaratan Sistem
- **Python 3.11+**
- **FFmpeg**: Diperlukan untuk konversi Video & Audio. ([Cara Install FFmpeg](https://ffmpeg.org/download.html))
- **Redis Server**: Diperlukan sebagai message broker untuk sistem antrian. ([Download Redis](https://github.com/tporadowski/redis/releases))
- **Microsoft Word**: Diperlukan jika ingin melakukan konversi Dokument (DOC/DOCX) di Windows secara akurat.

## 📥 Instalasi & Persiapan

### 1. Clone Repositori
```bash
git clone https://github.com/Gansputra/convertin.git
cd Convertin
```

### 2. Lingkungan Virtual (Virtual Environment)
**Untuk Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 3. Instal Dependensi
```bash
pip install -r requirements.txt
```

## ⚡ Cara Menjalankan
Aplikasi ini membutuhkan tiga komponen berjalan bersamaan:

### Langkah 1: Jalankan Redis Server
Pastikan `redis-server` aktif di komputer Anda (default port: 6379).

### Langkah 2: Jalankan Celery Worker (Terminal 1)
Buka terminal baru, aktifkan venv, lalu jalankan worker:
```bash
# Untuk Windows (menggunakan eventlet)
celery -A celery_worker.celery worker --loglevel=info -P eventlet
```

### Langkah 3: Jalankan Flask App (Terminal 2)
```bash
python app.py
```
Akses di browser: `http://127.0.0.1:5000`

## 📁 Struktur Proyek
- `app.py`: Main Flask application & API routes.
- `celery_worker.py`: Konfigurasi Celery dan background tasks.
- `converters/`: Modul logika untuk mesin konversi (Image, Video, Audio, Doc, Data).
- `logic/`: Mesin pintar (Recommendation Engine, Preset Manager, Estimation).
- `static/`: Aset frontend (CSS, JS, Icons).
- `templates/`: Antarmuka HTML dengan Tailwind CSS & Glassmorphism.
- `uploads/`: Penyimpanan sementara file masuk.
- `outputs/`: Hasil konversi siap unduh.

## 📝 Lisensi
Proyek ini dilisensikan di bawah [MIT License](LICENSE).

## 👨‍💻 Author
**gansputra**
* GitHub: [@Gansputra](https://github.com/Gansputra/)
* Instagram: [@gans.putra_](https://instagram.com/gans.putra_)

---
*Dibuat dengan Python, Flask, Celery, dan Cinta untuk efisiensi maksimal.*
