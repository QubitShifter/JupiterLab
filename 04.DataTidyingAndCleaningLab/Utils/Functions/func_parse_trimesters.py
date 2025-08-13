import re
from typing import Optional, Tuple


def parse_trimester(raw: str) -> Optional[Tuple[str, str]]:
    if not isinstance(raw, str):
        return None

    # Normalize spacing and lowercase
    raw = raw.strip().lower()

    # Match formats like "1T/2022", "4T2022", "4T/10", "4t72010", etc.
    match = re.search(r'([1-4])[tT][\/\s\-]?(\d{2,4})', raw)
    if match:
        quarter = int(match.group(1))
        year = int(match.group(2))

        # Normalize 2-digit year to 4-digit
        if year < 100:
            if year >= 50:
                year += 1900  # Assume 1950–1999
            else:
                year += 2000  # Assume 2000–2049

        quarter_months = {
            1: ("01-01", "03-31"),
            2: ("04-01", "06-30"),
            3: ("07-01", "09-30"),
            4: ("10-01", "12-31")
        }

        start, end = quarter_months.get(quarter, (None, None))
        if start and end:
            return f"{year}-{start}", f"{year}-{end}"

    return None
