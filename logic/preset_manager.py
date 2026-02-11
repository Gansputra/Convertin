class PresetManager:
    @staticmethod
    def get_preset_params(preset_name, target_format):
        """
        Returns FFmpeg parameters for a given preset and target format.
        Presets: 'high_quality', 'balanced', 'small_size'
        """
        target_format = target_format.lower()
        
        presets = {
            'high_quality': {
                'video': ['-c:v', 'libx264', '-crf', '18', '-preset', 'slow', '-c:a', 'aac', '-b:a', '320k'],
                'audio': ['-c:a', 'libmp3lame', '-q:a', '0'],
                'image': {'quality': 95}
            },
            'balanced': {
                'video': ['-c:v', 'libx264', '-crf', '23', '-preset', 'medium', '-c:a', 'aac', '-b:a', '192k'],
                'audio': ['-c:a', 'libmp3lame', '-q:a', '4'],
                'image': {'quality': 80}
            },
            'small_size': {
                'video': ['-c:v', 'libx265', '-crf', '28', '-preset', 'faster', '-vf', 'scale=-2:720', '-c:a', 'aac', '-b:a', '128k'],
                'audio': ['-c:a', 'libmp3lame', '-q:a', '7'],
                'image': {'quality': 60, 'optimize': True}
            }
        }
        
        selected = presets.get(preset_name, presets['balanced'])
        
        # Determine category
        video_formats = ['mp4', 'mkv', 'avi', 'mov']
        audio_formats = ['mp3', 'wav', 'm4a', 'flac', 'ogg']
        image_formats = ['jpg', 'jpeg', 'png', 'webp']
        
        if target_format in video_formats:
            return selected['video']
        elif target_format in audio_formats:
            return selected['audio']
        elif target_format in image_formats:
            return selected['image']
        
        return []
