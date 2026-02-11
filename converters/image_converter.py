import os
from PIL import Image
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

def convert_image(input_path, output_path, target_format, preset_params=None):
    try:
        target_format = target_format.upper()
        if target_format == 'JPG': 
            target_format = 'JPEG'

        if input_path.lower().endswith('.svg'):
            drawing = svg2rlg(input_path)
            renderPM.drawToFile(drawing, output_path, fmt="PNG")
            return True

        with Image.open(input_path) as img:
            if target_format == 'JPEG' and img.mode in ('RGBA', 'LA'):
                background = Image.new(img.mode[:-1], img.size, (255, 255, 255))
                background.paste(img, img.split()[-1])
                img = background.convert('RGB')
            
            save_params = {}
            if isinstance(preset_params, dict):
                save_params = preset_params
            
            img.save(output_path, format=target_format, **save_params)
            return True

    except Exception as e:
        print(f"[Image Error] {e}")
        return False