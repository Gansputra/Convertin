import os
from PIL import Image
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

def convert_image(input_path, output_path, target_format, preset_params=None, edit_params=None):
    try:
        from PIL import ImageDraw, ImageFont
        
        target_format = target_format.upper()
        if target_format == 'JPG': 
            target_format = 'JPEG'

        if input_path.lower().endswith('.svg'):
            drawing = svg2rlg(input_path)
            renderPM.drawToFile(drawing, output_path, fmt="PNG")
            img_path_for_pil = output_path # Work on the rendered PNG if further edits needed
        else:
            img_path_for_pil = input_path

        with Image.open(img_path_for_pil) as img:
            # Handle transparency for JPEG
            if target_format == 'JPEG' and img.mode in ('RGBA', 'LA'):
                background = Image.new(img.mode[:-1], img.size, (255, 255, 255))
                background.paste(img, img.split()[-1])
                img = background.convert('RGB')
            
            # Apply edits
            if edit_params:
                # 1. Auto Crop (simplified: center crop 80%)
                if edit_params.get('auto_crop'):
                    w, h = img.size
                    left = w * 0.1
                    top = h * 0.1
                    right = w * 0.9
                    bottom = h * 0.9
                    img = img.crop((left, top, right, bottom))

                # 2. Resize
                if edit_params.get('width') or edit_params.get('height'):
                    new_w = int(edit_params.get('width', img.size[0]))
                    new_h = int(edit_params.get('height', img.size[1]))
                    img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

                # 3. Watermark
                if edit_params.get('watermark_text'):
                    draw = ImageDraw.Draw(img)
                    # Try to use a default font
                    try:
                        font = ImageFont.truetype("arial.ttf", 36)
                    except:
                        font = ImageFont.load_default()
                    
                    text = edit_params['watermark_text']
                    # Position bottom-right
                    bbox = draw.textbbox((0, 0), text, font=font)
                    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
                    draw.text((img.size[0] - tw - 20, img.size[1] - th - 20), text, fill=(255, 255, 255, 128), font=font)

            save_params = {}
            if isinstance(preset_params, dict):
                save_params = preset_params
            
            img.save(output_path, format=target_format, **save_params)
            return True

    except Exception as e:
        print(f"[Image Error] {e}")
        return False