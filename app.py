import os
import uuid
from flask import Flask, render_template, request, send_from_directory, flash, redirect, url_for, jsonify
from werkzeug.utils import secure_filename

from celery_worker import convert_task, create_zip_task, celery
from celery.result import AsyncResult
from logic.recommendation_engine import RecommendationEngine
from logic.preset_manager import PresetManager
from converters import image_converter, audio_converter, video_converter, document_converter, data_converter

app = Flask(__name__)
app.secret_key = "kunci_rahasia_convertin"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
OUTPUT_FOLDER = os.path.join(BASE_DIR, 'outputs')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024 # Increased for batch 

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
    return render_template('index.html')

@app.route('/batch-upload', methods=['POST'])
def batch_upload():
    if 'files[]' not in request.files:
        return jsonify({'error': 'No files uploaded'}), 400
    
    files = request.files.getlist('files[]')
    formats = request.form.getlist('formats[]')
    presets = request.form.getlist('presets[]')
    edit_params_list = request.form.getlist('edit_params[]')
    
    if not files or not formats:
        return jsonify({'error': 'Missing data'}), 400
        
    batch_id = uuid.uuid4().hex[:8]
    batch_tasks = []
    
    import json
    for i, file in enumerate(files):
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = f"{batch_id}_{i}_{filename}"
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(input_path)
            
            target_format = formats[i]
            preset = presets[i] if i < len(presets) else 'balanced'
            
            # Parse edit_params if provided
            edit_params = None
            if i < len(edit_params_list) and edit_params_list[i]:
                try:
                    edit_params = json.loads(edit_params_list[i])
                except:
                    pass
            
            filename_no_ext = filename.rsplit('.', 1)[0]
            output_filename = f"converted_{filename_no_ext}_{uuid.uuid4().hex[:4]}.{target_format.lower()}"
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            
            # Start Celery Task with edit_params
            task = convert_task.delay(input_path, output_path, target_format, preset, edit_params=edit_params)
            batch_tasks.append({
                'task_id': task.id,
                'original_name': filename,
                'output_filename': output_filename
            })
            
    return jsonify({
        'batch_id': batch_id,
        'tasks': batch_tasks
    })

@app.route('/task-status/<task_id>')
def task_status(task_id):
    result = AsyncResult(task_id, app=celery)
    response = {
        'state': result.state,
        'info': result.info if result.state == 'PROGRESS' else (result.result if result.ready() else None)
    }
    return jsonify(response)

@app.route('/create-zip', methods=['POST'])
def create_zip():
    data = request.json
    batch_id = data.get('batch_id')
    output_filenames = data.get('filenames', [])
    
    if not output_filenames:
        return jsonify({'error': 'No files to zip'}), 400
        
    zip_filename = f"batch_{batch_id}_{uuid.uuid4().hex[:4]}.zip"
    zip_path = os.path.join(app.config['OUTPUT_FOLDER'], zip_filename)
    
    file_mappings = {name: os.path.join(app.config['OUTPUT_FOLDER'], name) for name in output_filenames}
    
    task = create_zip_task.delay(None, zip_path, file_mappings)
    return jsonify({'task_id': task.id, 'zip_filename': zip_filename})

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = f"temp_{uuid.uuid4().hex[:8]}_{filename}"
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(temp_path)
        
        try:
            analysis = RecommendationEngine.analyze_and_recommend(temp_path)
            analysis['temp_filename'] = unique_filename
            # Delete temp file after analysis is done
            if os.path.exists(temp_path):
                os.remove(temp_path)
            return jsonify(analysis)
        except Exception as e:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            return jsonify({'error': str(e)}), 500
            
    return jsonify({'error': 'File type not supported'}), 400

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    
    if not os.path.exists(file_path):
        flash("File tidak ditemukan atau sudah dihapus.", "error")
        return redirect(url_for('index'))

    def generate():
        with open(file_path, 'rb') as f:
            yield from f
        
        # Hapus file setelah stream selesai (file sudah tertutup)
        try:
            os.remove(file_path)
            print(f"[Cleanup] File output berhasil dihapus: {filename}")
        except Exception as e:
            print(f"[Cleanup Error] Gagal menghapus {filename}: {e}")

    return app.response_class(
        generate(),
        mimetype='application/octet-stream',
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

if __name__ == '__main__':
    app.run(debug=True)
