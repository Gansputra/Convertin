# Convertin ✨

**Convertin** adalah aplikasi web pengonversi file "all-in-one" berbasis Python Flask. Dilengkapi dengan antarmuka yang modern dan responsif, Convertin memungkinkan pengguna untuk mengonversi berbagai jenis format file mulai dari gambar, audio, video, hingga dokumen dan data dalam satu platform yang terintegrasi.

## 🚀 Fitur Utama

- **Gambar**: JPG, JPEG, PNG, WEBP, SVG.
- **Audio**: MP3, WAV, M4A, FLAC.
- **Video**: MP4, MKV.
- **Dokumen**: PDF, DOCX, DOC. (Dukungan konversi PDF <-> DOCX/DOC)
- **Data**: CSV, JSON, XLSX.
- **Modular**: Arsitektur kode yang rapi dengan pemisahan logika converter.
- **User Friendly**: Tampilan sederhana dan mudah digunakan.

## 🛠️ Persyaratan Sistem

- Python 3.11.
- Pip.

## 📥 Instalasi & Persiapan

Ikuti langkah-langkah berikut untuk menjalankan Convertin di komputer lokal Anda:

### 1. Clone Repositori (Opsional)
Jika Anda belum memiliki filenya, silakan clone atau unduh repositori ini.
```bash
git clone https://github.com/Gansputra/convertin.git
cd Convertin
```

### 2. Guard Lingkungan Virtual (Virtual Environment)
Sangat disarankan untuk menggunakan `venv` agar tidak mengganggu instalasi Python sistem Anda.

**Untuk Windows:**
```powershell
# Membuat virtual environment
python -m venv venv

# Mengaktifkan virtual environment
.\venv\Scripts\activate
```

**Untuk Linux/macOS:**
```bash
# Membuat virtual environment
python3 -m venv venv

# Mengaktifkan virtual environment
source venv/bin/activate
```

### 3. Instal Dependensi
Setelah venv aktif, instal semua pustaka yang diperlukan:
```bash
pip install -r requirements.txt
```

## 🏃 Menjalankan Aplikasi

Jalankan aplikasi dengan perintah:
```bash
python app.py
```

Setelah aplikasi berjalan, buka browser Anda dan akses alamat berikut:
```
http://127.0.0.1:5000
```

## 📁 Struktur Proyek
- `app.py`: Titik masuk utama aplikasi (Flask app).
- `converters/`: Berisi logika untuk masing-masing tipe konversi.
- `uploads/`: Folder penyimpanan sementara untuk file yang diunggah.
- `outputs/`: Folder penyimpanan untuk hasil konversi siap unduh.
- `templates/`: File HTML Jinja2.
- `static/`: File CSS, JS, dan gambar statis.

## 📝 Lisensi
Proyek ini dilisensikan di bawah [MIT License](LICENSE).

## 👨‍💻 Author

**gansputra**
* GitHub: [@Gansputra](https://github.com/Gansputra/)
* Instagram: [@gans.putra_](https://instagram.com/gans.putra_)

---
*Dibuat dengan Python & Tailwind CSS untuk tujuan edukasi.*
