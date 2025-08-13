from typing import Optional, Tuple
import pandas as pd
from dateutil import parser
import re
import calendar
from Utils.Dicts.dict_Es_to_En import es_to_en_map
from Utils.Dicts.dict_month_name_to_number  import month_name_to_number
from Utils.Functions.func_fix_harvest_date import parse_quarters
from Utils.Dicts.dict_Seasons import season_map
from Utils.Dicts.dict_Cofee_Harvest_periods import coffee_harvest_seasons

# Your translator stays the same
def translator(text):
    if not isinstance(text, str):
        return text
    text = re.sub(r'\ba\b', 'to', text, flags=re.IGNORECASE)
    for es, en in es_to_en_map.items():
        text = re.sub(rf'\b{es}\b', en, text, flags=re.IGNORECASE)
    return text.lower().strip()


def normalize_harvest_year(country, harvest_year, country_seasons=None):
    if not isinstance(harvest_year, str):
        return None, None

    # Step 1: Translate and normalize text
    harvest_year = translator(harvest_year)

    # Step 2: Try quarter-style first
    quarter_result = parse_quarters(harvest_year)
    if quarter_result:
        return quarter_result

    # Step 3: Match season keywords
    for season, (start_str, end_str) in season_map.items():
        if season in harvest_year:
            year_match = re.search(r'\d{4}', harvest_year)
            if year_match:
                year = int(year_match.group(0))
                # Handle winter spanning 2 years
                if season == "winter":
                    start_date = pd.Timestamp(f"{year}-12-01")
                    end_date = pd.Timestamp(f"{year+1}-02-28")
                else:
                    start_date = pd.Timestamp(f"{year}-{start_str}")
                    end_date = pd.Timestamp(f"{year}-{end_str}")
                return start_date, end_date

    # Step 4: Check for month range (e.g., April to August)
    match = re.match(r'([a-z]+)[\s\-–to]+([a-z]+)', harvest_year)
    if match:
        start_month, end_month = match.groups()
        try:
            start_month_num = int(month_name_to_number[start_month.lower()])
            end_month_num = int(month_name_to_number[end_month.lower()])
        except KeyError as e:
            print(f"DEBUG (month parse error): country={country}, period={harvest_year}, error='{e.args[0]}'")
            return None, None

        # Try to extract year from full string
        year_match = re.search(r'\d{4}', harvest_year)
        if year_match:
            year = int(year_match.group(0))
        else:
            year = 2010  # fallback if year not present

        try:
            start_date = pd.Timestamp(year=year, month=start_month_num, day=1)
            end_date = pd.Timestamp(year=year, month=end_month_num, day=28) + pd.offsets.MonthEnd(0)
            return start_date, end_date
        except Exception as e:
            print(f"DEBUG (Timestamp error): {e}")
            return None, None

    # Step 5: Handle YYYY or YYYY/YYYY formats
    year_range = [int(y[-4:]) for y in re.findall(r'\d{4,5}', harvest_year) if y[-4:].isdigit()]
    year_range = [y for y in year_range if 1900 <= y <= 2100]  # sanity check range
    if len(year_range) == 1:
        year = int(year_range[0])
        return pd.Timestamp(f"{year}-01-01"), pd.Timestamp(f"{year}-12-31")
    elif len(year_range) == 2:
        start, end = int(year_range[0]), int(year_range[1])
        return pd.Timestamp(f"{start}-01-01"), pd.Timestamp(f"{end}-12-31")

    # Step 6: Fallback to country default harvest period
    country = country.strip().title()
    if country_seasons:
        periods = country_seasons.get(country)
        if periods:
            for period in periods:
                translated_period = translator(period)
                match = re.match(r'([a-z]+)[\s\-–to]+([a-z]+)', translated_period)
                if match:
                    start_month, end_month = match.groups()
                    try:
                        start_month_num = int(month_name_to_number[start_month])
                        end_month_num = int(month_name_to_number[end_month])
                        fallback_year = 2010
                        start_date = pd.Timestamp(f"{fallback_year}-{start_month_num:02d}-01")
                        end_date = pd.Timestamp(f"{fallback_year}-{end_month_num:02d}-28") + pd.offsets.MonthEnd(0)
                        return start_date, end_date
                    except Exception as e:
                        print(f"DEBUG (fallback month error): {e}")
                        continue

    # Nothing matched
    print(f"DEBUG (unparsed): country={country}, harvest_year={harvest_year}")
    return None, None
