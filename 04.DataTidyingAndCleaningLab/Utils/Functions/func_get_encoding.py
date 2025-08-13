import chardet
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)
pd.set_option('display.precision', 2)

def encoding_pre_check(filepath, read_rows=False):
    """
    Detects encoding, prints details, and returns (encoding, dataframe).
    """
    try:
        with open(filepath, 'rb') as f:
            raw_data = f.read(100000)
            result = chardet.detect(raw_data)

        encoding = result['encoding']
        confidence = result['confidence']
        print(f"Detected encoding: {encoding} (confidence: {confidence:.2f})")

        try:
            df = pd.read_csv(filepath, encoding=encoding)
            print("CSV file loaded successfully using detected encoding.")
            if read_rows:
                print("\n Sample rows:\n", df.head(5))
            return encoding, df

        except UnicodeDecodeError as ude:
            print(f"UnicodeDecodeError: {ude}")
        except Exception as e:
            print(f"Error while reading CSV: {e}")

    except Exception as e:
        print(f"Failed to open/read file: {e}")

    return None, None
