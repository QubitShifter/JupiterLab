import pandas as pd
from utils.functions.func_helper_print_colors import color_print


def print_duplicate_rows(dataframe, indent="    ", subset=None):
    if subset:
        duplicates = dataframe[dataframe.duplicated(subset=subset, keep=False)]
    else:
        duplicates = dataframe[dataframe.duplicated(keep=False)]

    count = len(duplicates)
    color_print(f"Duplicate rows: {count}", level="warning")

    if count > 0:
        color_print(f"Duplicate entries preview:", level="warning")
        if subset:
            print(duplicates[subset].head(10))
        else:
            print(duplicates.head(10))
