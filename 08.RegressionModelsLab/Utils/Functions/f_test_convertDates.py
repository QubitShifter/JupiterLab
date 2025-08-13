from Utils.Functions.func_parse_date_range import parse_date_range


def convertDates():
    test_dates = [
        "Mayo a Julio",
        "April 2010",
        "23 July 2010",
        "Fall 2009",
        "Abril - Julio /2011",
        "2013/2014",
        "4T/2011",
        "Spring 2011 in Colombia",
        "May–August 2010",
        "June to September",
        "January / April 2012",
        None,
        "",
        "unknown"
    ]

    for date in test_dates:
        result = parse_date_range(date)
        print(f"{date!r:35} -> {result} ")


print(convertDates())

