import subprocess
import os

def convert_audio(input_path, output_path, target_format, preset_params=None):
    try:
        # Ensure paths use Windows backslashes
        abs_input = os.path.abspath(input_path).replace('/', '\\')
        abs_output = os.path.abspath(output_path).replace('/', '\\')

        command = ['ffmpeg', '-i', abs_input]
        
        if preset_params:
            command.extend(preset_params)
            
        command.extend(['-y', abs_output])

        # Use DEVNULL to prevent hang
        result = subprocess.run(
            command, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            return True
        else:
            print(f"[Audio FFmpeg Error] {result.stderr}")
            return False

    except Exception as e:
        print(f"[Audio Error] {e}")
        return False