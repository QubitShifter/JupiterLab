import re

def snake_case(column: str) -> str:
    col = column.strip()

    if col.lower() == "unnamed: 0":
        return col.lower()
    col = re.sub(r"[ /\\.]+", "_", col)
    col = re.sub(r"_+", "_", col)
    col = col.strip("_")

    return col.lower()
