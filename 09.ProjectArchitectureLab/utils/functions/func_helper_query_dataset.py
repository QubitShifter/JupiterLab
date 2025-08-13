import chardet
import pandas as pd
import os
from utils.functions.func_helper_print_colors import color_print
from utils.functions.func_helper_duplicate_rows import print_duplicate_rows


def query_dataframe(dataframe, filepath=None, encoding=None, indent="    "):
    # Encoding + filepath diagnostics
    if filepath:
        if encoding:
            color_print(f"{indent}Encoding check:", level="info")
            print(f"{'':48}")
            color_print(f"{indent} Filepath: {filepath}", level="info")
            color_print(f"{indent} Encoding: {encoding}", level="info")
        else:
            color_print(f"{indent} Filepath provided but no encoding specified.", level="yellow")

        # Skip raw reading if ZIP
        if filepath.lower().endswith('.zip'):
            color_print(f"{indent} Skipping raw line count: ZIP file detected.", level="info")
        else:
            try:
                with open(filepath, 'r', encoding=encoding or 'utf-8') as f:
                    total_lines = sum(1 for _ in f)
                color_print(f"{indent} Total lines in file (including header): {total_lines}", level="info")
                color_print(f"{indent} Rows loaded in DataFrame: {dataframe.shape[0]}", level="info")
                if dataframe.shape[0] < total_lines - 1:
                    color_print(f"{indent} Warning: Some rows may not have been read.", level="yellow")
            except Exception as e:
                color_print(f"{indent} Could not read raw file to count lines: {e}", level="yellow")
    else:
        color_print(f"{indent}No filepath provided.", level="yellow")

    # Basic info
    print(f"{'':48}\n" * 2)
    color_print("Dataset Summary:", level="info")
    color_print(f"DataFrame dimensions: {dataframe.shape}", level="info")
    print(f"{'':48}")

    # Null values
    print(f"{'':48}\n" * 2)
    nulls = dataframe.isnull().sum()
    if nulls.sum() > 0:
        color_print("Missing values per column:", level="warning")
        print(f"{'':48}")
        print(nulls[nulls > 0])
    else:
        color_print("No missing values detected.", level="info")
    print(f"{'':48}")

    # Duplicates
    print(f"{'':48}\n" * 2)
    print_duplicate_rows(dataframe)
    print(f"{'':48}")

    # Columns and dtypes
    print(f"{'':48}\n" * 2)
    color_print(f"\n{indent}Columns and data types:", level="info")
    for col, dtype in dataframe.dtypes.items():
        print(f"{indent}  - {col}: {dtype}")

    # Column listing
    print(f"{'':48}\n" * 2)
    color_print("Column names (grouped) for easy reading:", level="info")
    cols = list(dataframe.columns)
    for i in range(0, len(cols), 5):
        print(indent + "  " + str(cols[i:i + 5]))

    # Preview rows
    print(f"{'':48}\n" * 2)
    color_print("First 5 rows:", level="info")
    print(dataframe.head())
    print(f"{'':48}\n")
    color_print("Last 5 rows:", level="info")
    print(dataframe.tail())

    # # Summary stats
    # print(f"{'':48}\n" * 2)
    # color_print(f"Descriptive statistics:", level="info")
    # print(dataframe.describe(include='all'))
