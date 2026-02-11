import eventlet
eventlet.monkey_patch()

import os
import zipfile
from celery import Celery
from converters import image_converter, audio_converter, video_converter, document_converter, data_converter
from logic.preset_manager import PresetManager

BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

celery = Celery('convertin', broker=BROKER_URL, backend=RESULT_BACKEND)

CONVERTER_MAP = {
    'jpg': image_converter.convert_image,
    'jpeg': image_converter.convert_image,
    'png': image_converter.convert_image,
    'webp': image_converter.convert_image,
    'svg': image_converter.convert_image,
    'mp3': audio_converter.convert_audio,
    'wav': audio_converter.convert_audio,
    'm4a': audio_converter.convert_audio,
    'flac': audio_converter.convert_audio,
    'mp4': video_converter.convert_video,
    'mkv': video_converter.convert_video,
    'pdf': document_converter.convert_document,
    'docx': document_converter.convert_document,
    'doc': document_converter.convert_document,
    'csv': data_converter.convert_data,
    'json': data_converter.convert_data,
    'xlsx': data_converter.convert_data
}

@celery.task(bind=True)
def convert_task(self, input_path, output_path, target_format, preset, edit_params=None):
    """
    Background task to convert a single file.
    """
    print(f"[DEBUG Worker] Task started for: {input_path}")
    if not os.path.exists(input_path):
        print(f"[ERROR Worker] File NOT FOUND: {input_path}")
        return {'status': 'error', 'message': f'Input file not found: {input_path}'}

    self.update_state(state='PROGRESS', meta={'progress': 10})
    
    file_ext = os.path.splitext(input_path)[1].lower()[1:]
    converter_function = CONVERTER_MAP.get(file_ext)
    
    if not converter_function:
        return {'status': 'error', 'message': f'No converter for {file_ext}'}
        
    try:
        self.update_state(state='PROGRESS', meta={'progress': 30})
        preset_params = PresetManager.get_preset_params(preset, target_format)
        
        self.update_state(state='PROGRESS', meta={'progress': 50})
        # Pass both preset_params and edit_params
        success = converter_function(
            input_path, 
            output_path, 
            target_format, 
            preset_params=preset_params,
            edit_params=edit_params
        )
        
        if success:
            self.update_state(state='PROGRESS', meta={'progress': 100})
            return {'status': 'success', 'filename': os.path.basename(output_path)}
        else:
            return {'status': 'error', 'message': 'Conversion failed'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

@celery.task
def create_zip_task(batch_dir, output_zip_path, file_mappings):
    """
    Creates a ZIP file for a batch of converted files.
    """
    try:
        with zipfile.ZipFile(output_zip_path, 'w') as zf:
            for original_name, converted_path in file_mappings.items():
                if os.path.exists(converted_path):
                    # We use the converted filename in the zip
                    zf.write(converted_path, arcname=os.path.basename(converted_path))
        return {'status': 'success', 'zip_filename': os.path.basename(output_zip_path)}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
