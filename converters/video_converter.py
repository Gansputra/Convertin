import subprocess
import os

def convert_video(input_path, output_path, target_format, preset_params=None, edit_params=None):
    try:
        # Ensure paths use Windows backslashes
        abs_input = os.path.abspath(input_path).replace('/', '\\')
        abs_output = os.path.abspath(output_path).replace('/', '\\')

        command = ['ffmpeg', '-y']

        # Handling inputs and filters
        input_args = []
        if edit_params:
            if edit_params.get('trim_start'):
                input_args.extend(['-ss', str(edit_params['trim_start'])])
            if edit_params.get('trim_end'):
                input_args.extend(['-to', str(edit_params['trim_end'])])
        
        command.extend(input_args)
        command.extend(['-i', abs_input])

        # Video filters and settings
        vfilters = []
        if edit_params:
            if edit_params.get('resolution'):
                res = edit_params['resolution']
                if res == '720p': vfilters.append('scale=1280:720')
                elif res == '480p': vfilters.append('scale=854:480')
                elif res == '360p': vfilters.append('scale=640:360')
            
            if edit_params.get('extract_audio'):
                command.append('-vn')

        if vfilters:
            command.extend(['-vf', ','.join(vfilters)])

        if preset_params:
            command.extend(preset_params)
        elif target_format.lower() == 'gif':
            if not vfilters: # Only add if not already scaling
                command.extend(['-vf', 'fps=10,scale=320:-1:flags=lanczos'])
        elif target_format.lower() == 'mp3':
            command.extend(['-q:a', '0', '-map', 'a'])
        else:
            # Default for video
            if not any(arg in command for arg in ['-c:v', '-vn']):
                command.extend(['-c:v', 'libx264', '-preset', 'fast'])

        command.append(abs_output)

        print(f"[Video] Running command: {' '.join(command)}")

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