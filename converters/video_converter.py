import subprocess
import os

def convert_video(input_path, output_path, target_format):
    try:
        command = ['ffmpeg', '-i', input_path]

        if target_format.lower() == 'gif':
            command.extend(['-vf', 'fps=10,scale=320:-1:flags=lanczos', '-y', output_path])
        
        elif target_format.lower() == 'mp3':
            command.extend(['-q:a', '0', '-map', 'a', '-y', output_path])
            
        else:
            command.extend(['-c:v', 'libx264', '-preset', 'fast', '-y', output_path])

        result = subprocess.run(
            command, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )

        if result.returncode == 0:
            return True
        else:
            print(f"[Video FFmpeg Error] {result.stderr.decode()}")
            return False

    except Exception as e:
        print(f"[Video Error] {e}")
        return False