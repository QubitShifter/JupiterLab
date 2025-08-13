import pandas as pd


def convert_date_format(df: pd.DataFrame, date_column: str = 'Date') -> pd.DataFrame:
    df = df.copy()
    df[date_column] = pd.to_datetime(df[date_column], error = 'coerce')
    return df