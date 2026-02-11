import subprocess
import os

def convert_audio(input_path, output_path, target_format, preset_params=None, edit_params=None):
    try:
        # Ensure paths use Windows backslashes
        abs_input = os.path.abspath(input_path).replace('/', '\\')
        abs_output = os.path.abspath(output_path).replace('/', '\\')

        command = ['ffmpeg', '-y']

        # Handling inputs (trimming happens at input level for efficiency)
        if edit_params:
            if edit_params.get('trim_start'):
                command.extend(['-ss', str(edit_params['trim_start'])])
            if edit_params.get('trim_end'):
                command.extend(['-to', str(edit_params['trim_end'])])

        command.extend(['-i', abs_input])

        # Audio filters
        afilters = []
        if edit_params:
            if edit_params.get('noise_reduction'):
                # Simple afftdn (Audio FFT De-Noise)
                afilters.append('afftdn')
        
        if afilters:
            command.extend(['-af', ','.join(afilters)])
        
        if preset_params:
            command.extend(preset_params)
            
        command.append(abs_output)

        print(f"[Audio] Running command: {' '.join(command)}")

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