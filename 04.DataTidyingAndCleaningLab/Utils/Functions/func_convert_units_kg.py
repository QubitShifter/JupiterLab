import re
import pandas as pd


def units_to_kg(value):
    if pd.isna(value):
        return None

    # convert to string and clean
    unitString = str(value).lower().strip().replace(" ", "")

    if "kg,lbs" in unitString:
        matchValue = re.match(r"([0-9\.]+)", unitString)
        if matchValue:
            return round(float(matchValue.group(1)))
        else:
            return None

    if unitString in ["0", "0kg", "0lbs"]:
        return 0

    matchValue = re.match(r"([0-9\.]+)", unitString)
    if not matchValue:
        return None

    num = float(matchValue.group(1))

    if "kg" in unitString:
        return round(num)
    elif "lbs" in unitString:
        return round(num * 0.453592)
    else:
        return round(num)
