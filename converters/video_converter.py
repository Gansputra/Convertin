import subprocess
import os

def convert_video(input_path, output_path, target_format, preset_params=None):
    try:
        command = ['ffmpeg', '-i', input_path]

        if preset_params:
            command.extend(preset_params)
        elif target_format.lower() == 'gif':
            command.extend(['-vf', 'fps=10,scale=320:-1:flags=lanczos'])
        elif target_format.lower() == 'mp3':
            command.extend(['-q:a', '0', '-map', 'a'])
        else:
            command.extend(['-c:v', 'libx264', '-preset', 'fast'])

        command.extend(['-y', output_path])

        # Ensure paths use Windows backslashes
        abs_input = os.path.abspath(input_path).replace('/', '\\')
        abs_output = os.path.abspath(output_path).replace('/', '\\')

        command = ['ffmpeg', '-i', abs_input]

        if preset_params:
            command.extend(preset_params)
        elif target_format.lower() == 'gif':
            command.extend(['-vf', 'fps=10,scale=320:-1:flags=lanczos'])
        elif target_format.lower() == 'mp3':
            command.extend(['-q:a', '0', '-map', 'a'])
        else:
            command.extend(['-c:v', 'libx264', '-preset', 'fast'])

        command.extend(['-y', abs_output])

        print(f"[Video] Running command: {' '.join(command)}")

        # Use DEVNULL to prevent pipe buffer from filling up and hanging
        result = subprocess.run(
            command, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode == 0:
            return True
        else:
            print(f"[Video FFmpeg Error] {result.stderr}")
            return False

    except Exception as e:
        print(f"[Video Error] {e}")
        return False