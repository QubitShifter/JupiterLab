import pandas as pd


def fix_dates(df, column_name, output_format='%Y-%m-%d'):
    df = df.copy()
    df['parsed_date'] = pd.to_datetime(df[column_name], errors='coerce')
    df['invalid_date'] = df['parsed_date'].isna()
    df['parsed_date'] = df['parsed_date'].dt.strftime(output_format)
    df[column_name] = df['parsed_date']
    df.drop(columns=['parsed_date'], inplace=True)

    return df

