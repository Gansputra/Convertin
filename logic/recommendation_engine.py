import subprocess
import json
import os
from PIL import Image
from logic.estimation_engine import EstimationEngine
from logic.preset_manager import PresetManager

class RecommendationEngine:
    @staticmethod
    def get_metadata(file_path):
        """
        Extracts metadata using ffprobe and Pillow.
        """
        ext = os.path.splitext(file_path)[1].lower()[1:]
        metadata = {
            'size': os.path.getsize(file_path),
            'format': ext,
            'type': 'unknown',
            'bitrate': 0,
            'resolution': 'N/A'
        }
        
        # Audio/Video metadata via ffprobe
        media_exts = ['mp4', 'mkv', 'avi', 'mov', 'mp3', 'wav', 'm4a', 'flac']
        if ext in media_exts:
            try:
                cmd = [
                    'ffprobe', '-v', 'quiet', '-print_format', 'json', 
                    '-show_format', '-show_streams', file_path
                ]
                result = subprocess.run(cmd, capture_output=True, text=True)
                data = json.loads(result.stdout)
                
                if 'format' in data:
                    metadata['duration'] = float(data['format'].get('duration', 0))
                    metadata['bitrate'] = int(data['format'].get('bit_rate', 0))
                
                for stream in data.get('streams', []):
                    if stream.get('codec_type') == 'video':
                        metadata['type'] = 'video'
                        metadata['width'] = int(stream.get('width', 0))
                        metadata['height'] = int(stream.get('height', 0))
                        metadata['resolution'] = f"{metadata['width']}x{metadata['height']}"
                    elif stream.get('codec_type') == 'audio' and metadata['type'] == 'unknown':
                        metadata['type'] = 'audio'
            except Exception as e:
                print(f"Metadata extraction error: {e}")

        # Image metadata via Pillow
        image_exts = ['jpg', 'jpeg', 'png', 'webp', 'svg']
        if ext in image_exts:
            metadata['type'] = 'image'
            try:
                with Image.open(file_path) as img:
                    metadata['width'], metadata['height'] = img.size
                    metadata['resolution'] = f"{metadata['width']}x{metadata['height']}"
            except:
                pass
                
        # Document metadata
        doc_exts = ['pdf', 'docx', 'doc', 'txt']
        if ext in doc_exts:
            metadata['type'] = 'document'
            
        return metadata

    @classmethod
    def analyze_and_recommend(cls, file_path):
        metadata = cls.get_metadata(file_path)
        file_type = metadata['type']
        
        recommendations = []
        
        if file_type == 'video':
            # Check bitrate for smarter recommendation
            high_bitrate = metadata.get('bitrate', 0) > 5000000 # > 5Mbps
            if high_bitrate:
                recommendations.append(cls._build_rec(metadata, 'mp4', 'balanced', "Bitrate asli cukup tinggi. Kompresi seimbang akan menghemat banyak ruang tanpa merusak visual."))
                recommendations.append(cls._build_rec(metadata, 'mp4', 'small_size', "Optimalkan ukuran secara agresif untuk penggunaan di web/chat."))
            else:
                recommendations.append(cls._build_rec(metadata, 'mp4', 'high_quality', "File asli sudah cukup efisien. Gunakan preset kualitas tinggi untuk menjaga detail."))
                recommendations.append(cls._build_rec(metadata, 'mp4', 'balanced', "Keseimbangan standar untuk pengiriman file yang lebih cepat."))

        elif file_type == 'audio':
            is_lossless = metadata['format'] in ['wav', 'flac']
            if is_lossless:
                recommendations.append(cls._build_rec(metadata, 'mp3', 'high_quality', "Konversi lossless ke MP3 320kbps memberikan efisiensi ruang hingga 80% dengan kualitas auditif yang sulit dibedakan."))
                recommendations.append(cls._build_rec(metadata, 'm4a', 'balanced', "Format AAC (M4A) lebih efisien dari MP3 untuk ukuran file yang sama."))
            else:
                recommendations.append(cls._build_rec(metadata, 'mp3', 'balanced', "Standar industri untuk kompatibilitas dan ukuran file yang ringkas."))

        elif file_type == 'image':
            large_image = metadata.get('size', 0) > 2000000 # > 2MB
            if large_image:
                recommendations.append(cls._build_rec(metadata, 'webp', 'balanced', "Format WebP menawarkan kompresi superior dibanding JPG/PNG untuk gambar berukuran besar."))
            else:
                recommendations.append(cls._build_rec(metadata, 'jpg', 'high_quality', "Jaga kompatibilitas maksimal dengan tetap mempertahankan detail tajam."))

        else:
            recommendations.append({
                'target_format': 'pdf' if file_type == 'document' else metadata['format'],
                'preset': 'balanced',
                'reason': "Optimasi dokumen untuk portabilitas lintas perangkat.",
                'estimation': EstimationEngine.estimate_output(metadata, 'pdf', 'balanced')
            })

        return {
            'metadata': metadata,
            'recommendations': recommendations
        }

    @staticmethod
    def _build_rec(metadata, target_format, preset, reason):
        return {
            'target_format': target_format,
            'preset': preset,
            'reason': reason,
            'estimation': EstimationEngine.estimate_output(metadata, target_format, preset)
        }
