import pandas as pd
import unicodedata


def normalize_text(s):
    if pd.isna(s):
        return None
    s = s.strip().lower()
    s = unicodedata.normalize('NFKD', s)
    return s
