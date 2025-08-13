def remove_commas(df, column_name, to_type=float, suppress_scientific_display=True):
    """
       Removes commas and converts a column to a numeric type (float or int).
       Optionally suppresses scientific notation in display.
    """
    df[column_name] = (
        df[column_name]
        .astype(str)                      # Ensure it's string
        .str.replace(',', '', regex=False)
        .astype(to_type)
    )
    return df

    if suppress_scientific_display and to_type == float:
        pd.set_option('display.float_format', '{:,.0f}'.format)
    return df
