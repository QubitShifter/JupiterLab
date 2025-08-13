import re


def normalize_dates(text):
    if not isinstance(text, str):
        return text

    text = text.lower().strip()
    # Replace common separators with consistent format
    text = re.sub(r'\s+to\s+|\s*-\s*', ' - ', text)
    text = re.sub(r'\s*/\s*', ' / ', text)
    text = re.sub(r'\s+', ' ', text)  # Clean up extra whitespace
    return text
