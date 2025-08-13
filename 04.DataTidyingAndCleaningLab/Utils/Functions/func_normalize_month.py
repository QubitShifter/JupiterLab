import re


def normalize_month(text):
    if not isinstance(text, str):
        return text  # Leave as is (e.g. NaN, numbers)

    original = text  # Keep a copy in case we don't touch it

    # Normalize connector words
    text = re.sub(r'\b(to|through)\b', '-', text, flags=re.IGNORECASE)

    # Month name normalization
    months = [
        'january', 'february', 'march', 'april', 'may', 'june',
        'july', 'august', 'september', 'october', 'november', 'december'
    ]

    for month in months:
        text = re.sub(rf'\b{month}\b', month.capitalize(), text, flags=re.IGNORECASE)

    # Clean spacing around dashes
    text = re.sub(r'\s*-\s*', ' - ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    return text if text else original
