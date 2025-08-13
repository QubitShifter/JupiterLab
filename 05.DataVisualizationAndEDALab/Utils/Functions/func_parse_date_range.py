import re
from dateutil import parser
from typing import Optional, Tuple
from Utils.Dicts.dict_Seasons import season_map
from Utils.Functions.func_parse_quaters import parse_quarters
from Utils.Functions.func_spanish_to_english import translator


def parse_date_range(raw: str) -> Optional[Tuple[str, str]]:
    if not isinstance(raw, str):
        return None

    raw = translator(raw).strip().lower()

    # 1. Try parsing quarter-like strings
    quarter_result = parse_quarters(raw)
    if quarter_result:
        return quarter_result

    for season, (start_suffix, end_suffix) in season_map.items():
        if season in raw:
            year_match = re.search(r'(\d{4})', raw)
            if year_match:
                year = int(year_match.group(1))
                if season == "winter":
                    return f"{year}-12-01", f"{year+1}-02-28"
                return f"{year}-{start_suffix}", f"{year}-{end_suffix}"

    # 3. Handle single-month entries (e.g. "April 2010")
    if re.match(r'^[a-zA-Z]+\s+\d{4}$', raw):
        try:
            dt = parser.parse(raw)
            start = dt.replace(day=1)
            next_month = start.replace(day=28) + pd.Timedelta(days=4)
            end = next_month - pd.Timedelta(days=next_month.day)
            return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")
        except:
            pass

    # 4. Handle date ranges using separators
    separators = [' to ', ' a ', '-', '–', '—', '/', '–']
    for sep in separators:
        if sep in raw:
            parts = [p.strip() for p in raw.split(sep)]
            if len(parts) == 2:
                try:
                    start = parser.parse(parts[0], fuzzy=True, default=parser.parse("2000-01-01"))
                    end = parser.parse(parts[1], fuzzy=True, default=parser.parse("2000-01-01"))

                    # Inherit year from other side if missing
                    if start.year == 2000 and end.year != 2000:
                        start = start.replace(year=end.year)
                    elif end.year == 2000 and start.year != 2000:
                        end = end.replace(year=start.year)

                    # Fix reversed dates
                    if start > end:
                        start, end = end, start

                    return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")
                except:
                    return None

    # 5. Handle a single date string
    try:
        single_date = parser.parse(raw, fuzzy=True)
        return single_date.strftime("%Y-%m-%d"), single_date.strftime("%Y-%m-%d")
    except:
        return None
