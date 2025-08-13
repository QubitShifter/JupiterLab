from Utils.Functions.func_fix_date_format import fix_dates


def convert_date_multiColumns(df, column_names, output_format='%Y-%m-%d'):
    df = df.copy()
    for column in column_names:
        df = fix_dates(df, column, output_format)
    return df
