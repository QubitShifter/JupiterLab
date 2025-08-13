import zipfile
import chardet
import pandas as pd
from Utils.Functions.func_helper_print_colors import color_print


def read_zipped_csv(zip_path):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            # Find the first .csv file in the archive
            csv_files = [f for f in zf.namelist() if f.endswith('.csv')]
            if not csv_files:
                color_print("No CSV file found in ZIP.", level="success")
                return None

            csv_name = csv_files[0]
            color_print(f"Found CSV in ZIP: {csv_name}", level="info")

            # Detect encoding
            with zf.open(csv_name) as f:
                raw_data = f.read(100000)
                result = chardet.detect(raw_data)
                encoding = result['encoding']
                color_print(f"Detected encoding: {encoding}", level="info")

            # Load CSV
            with zf.open(csv_name) as f:
                df = pd.read_csv(f, encoding=encoding)

                color_print("CSV loaded successfully.", level="info")
            print(f"{'':48}")
            return df

    except Exception as e:
        color_print(f"Error reading ZIP: {e}", level="error")
        return None
