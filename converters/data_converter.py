import pandas as pd
import os

def convert_data(input_path, output_path, target_format, preset_params=None):
    try:
        ext = os.path.splitext(input_path)[1].lower()
        
        if ext == '.csv':
            df = pd.read_csv(input_path)
        elif ext == '.xlsx':
            df = pd.read_excel(input_path)
        elif ext == '.json':
            df = pd.read_json(input_path)
        else:
            return False
        target = target_format.lower()
        
        if target == 'csv':
            df.to_csv(output_path, index=False)
        elif target == 'xlsx':
            df.to_excel(output_path, index=False)
        elif target == 'json':
            df.to_json(output_path, orient='records')
        else:
            return False

        return True

    except Exception as e:
        print(f"[Data Error] {e}")
        return False