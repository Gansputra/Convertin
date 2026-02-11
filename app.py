import os
import uuid
from flask import Flask, render_template, request, send_from_directory, flash, redirect, url_for
from werkzeug.utils import secure_filename

from converters import image_converter, audio_converter, video_converter, document_converter, data_converter

app = Flask(__name__)
app.secret_key = "kunci_rahasia_convertin"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
OUTPUT_FOLDER = os.path.join(BASE_DIR, 'outputs')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

CONVERTER_MAP = {
    # Images
    'jpg': image_converter.convert_image,
    'jpeg': image_converter.convert_image,
    'png': image_converter.convert_image,
    'webp': image_converter.convert_image,
    'svg': image_converter.convert_image,
    # Audio
    'mp3': audio_converter.convert_audio,
    'wav': audio_converter.convert_audio,
    'm4a': audio_converter.convert_audio,
    'flac': audio_converter.convert_audio,
    # Video
    'mp4': video_converter.convert_video,
    'mkv': video_converter.convert_video,
    # Documents
    'pdf': document_converter.convert_document,
    'docx': document_converter.convert_document,
    'doc': document_converter.convert_document,
    # Data
    'csv': data_converter.convert_data,
    'json': data_converter.convert_data,
    'xlsx': data_converter.convert_data
}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in CONVERTER_MAP

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Tidak ada file yang dipilih')
            return redirect(request.url)
        
        file = request.files['file']
        target_format = request.form.get('format')
        
        if file.filename == '':
            flash('Nama file kosong')
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex[:8]}_{filename}"
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(input_path)
            
            file_ext = filename.rsplit('.', 1)[1].lower()
            filename_no_ext = filename.rsplit('.', 1)[0]
            output_filename = f"converted_{filename_no_ext}.{target_format.lower()}"
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            
            converter_function = CONVERTER_MAP.get(file_ext)
            
            if converter_function:
                try:
                    success = converter_function(input_path, output_path, target_format)
                    
                    if success:
                        flash(f"Berhasil! File dikonversi ke {target_format.upper()}", "success")
                        return render_template('index.html', download_file=output_filename)
                    else:
                        flash("Gagal melakukan konversi. Cek log untuk detail.", "error")
                except Exception as e:
                    flash(f"Terjadi kesalahan sistem: {str(e)}", "error")
            else:
                flash("Tipe file tidak didukung.", "error")
                
    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)