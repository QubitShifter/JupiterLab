def snake_case(column):
    if column.lower() == "unnamed: 0":
        return column.lower()
    return(
        column.replace('-', '_')
              .replace(' ', '_')
              .replace('.', '_')
              .lower()
    )
