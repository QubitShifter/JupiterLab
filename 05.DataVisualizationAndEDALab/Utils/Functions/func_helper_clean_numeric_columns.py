import pandas as pd


def clean_numeric_columns(df, columns, to_type=float, replace_nans=True):
    for col in columns:
        df[col] = (
            df[col].astype(str).str.replace(",", "", regex=False)
        )
        if replace_nans:
            df[col] = df[col].replace(["NaN", "nan"], pd.NA)

        df[col] = pd.to_numeric(df[col], errors='coerce').astype(to_type)

    return df
