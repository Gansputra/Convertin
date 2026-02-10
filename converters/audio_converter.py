import subprocess
import os

def convert_audio(input_path, output_path, target_format):
    try:
        command = [
            'ffmpeg', 
            '-i', input_path,
            '-y', 
            output_path
        ]
        result = subprocess.run(
            command, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        if result.returncode == 0:
            return True
        else:
            print(f"[Audio FFmpeg Error] {result.stderr.decode()}")
            return False

    except Exception as e:
        print(f"[Audio Error] {e}")
        return False