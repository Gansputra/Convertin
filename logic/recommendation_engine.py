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
            'type': 'unknown'
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
            recommendations.append(cls._build_rec(metadata, 'mp4', 'balanced', "Format universal dengan keseimbangan kualitas dan ukuran."))
            recommendations.append(cls._build_rec(metadata, 'mkv', 'high_quality', "Simpan kualitas asli dengan dukungan track audio ganda."))
            recommendations.append(cls._build_rec(metadata, 'mp4', 'small_size', "Optimalkan untuk pengiriman via chat atau hemat storage."))
        elif file_type == 'audio':
            recommendations.append(cls._build_rec(metadata, 'mp3', 'high_quality', "Kualitas audio terbaik untuk koleksi musik."))
            recommendations.append(cls._build_rec(metadata, 'm4a', 'balanced', "Efisiensi tinggi, cocok untuk perangkat seluler."))
        elif file_type == 'image':
            recommendations.append(cls._build_rec(metadata, 'webp', 'balanced', "Format modern dengan kompresi luar biasa tanpa kehilangan kualitas."))
            recommendations.append(cls._build_rec(metadata, 'jpg', 'high_quality', "Kompatibilitas maksimum untuk semua perangkat."))
        else:
            # Fallback
            recommendations.append({
                'target_format': 'pdf',
                'preset': 'balanced',
                'reason': "Format standar dokumen untuk portabilitas.",
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
