FORMAT_MAPPING = {
    'image': {
        'extensions': ['jpg', 'jpeg', 'png', 'webp', 'svg'],
        'targets': ['JPG', 'PNG', 'WEBP']
    },
    'audio': {
        'extensions': ['mp3', 'wav', 'm4a', 'flac'],
        'targets': ['MP3', 'WAV']
    },
    'video': {
        'extensions': ['mp4', 'mkv'],
        'targets': ['MP4', 'MKV', 'GIF', 'MP3']
    },
    'document': {
        'extensions': ['pdf', 'docx'],
        'targets': ['PDF', 'DOCX', 'JPG']
    },
    'data': {
        'extensions': ['csv', 'xlsx', 'json'],
        'targets': ['CSV', 'XLSX', 'JSON']
    }
}

def get_file_category(extension):
    extension = extension.lower()
    for category, data in FORMAT_MAPPING.items():
        if extension in data['extensions']:
            return category, data['targets']
    return None, []