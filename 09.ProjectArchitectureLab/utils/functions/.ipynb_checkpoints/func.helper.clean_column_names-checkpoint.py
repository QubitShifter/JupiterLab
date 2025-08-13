import pandas as pd

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns
        .str.strio()
        .str.replace(r"\s+", "_", regex = True)
        .str.replace("/", "_")
        .str.replace(".", "", regex = False)
    )

    return df