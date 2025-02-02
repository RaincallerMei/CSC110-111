"""CSC110 Fall 2024 Assignment 2, Part 1: Subway Delays

Module Description
==================
Write your functions for Part 1 in this file.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC110 Teaching Team
"""
import csv
import datetime


def read_csv_file(filename: str) -> tuple[list[str], list[list]]:
    """Return the headers and data stored in a csv file with the given filename.

    The return value is a tuple consisting of two elements:

    - The first is a list of strings for the headers of the csv file.
    - The second is a list of lists, where each inner list stores a row
      in the csv file. The types of the elements correspond to the
      appropriate data types for the TTC data.

    Note: you must complete process_row below and use it as a helper function
    in this function body.

    Preconditions:
      - filename refers to a valid csv file with headers
        (notice that we can't express this as a Python expression)

    >>> read_csv_file('oneline.csv')
    (['Date', 'Time', 'Day', 'Station', 'Code', 'Min Delay', 'Min Gap', 'Bound', 'Line', 'Vehicle'], \
[[datetime.date(2014, 1, 1), datetime.time(0, 21), 'Wednesday', 'VICTORIA PARK STATION', 'MUPR1', 55, 60, 'W', \
'BD', 5111]])
    """
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        data = [process_row(row) for row in reader]
    return (headers, data)


def process_row(row: list[str]) -> list:
    """Convert a row of subway delay data to a list with more appropriate data types.

    Notes:
    - You can use int(...) to convert from a string to an integer
    - You must complete the str_to_date and str_to_time functions below
      and use them here.

    Preconditions:
        - row has the correct format for the TTC subway delay data set

    >>> process_row(['01/01/2014', '00:21', 'Wednesday', 'VICTORIA PARK STATION', 'MUPR1', '55', '60', 'W', 'BD', \
'5111'])
    [datetime.date(2014, 1, 1), datetime.time(0, 21), 'Wednesday', 'VICTORIA PARK STATION', 'MUPR1', 55, 60, 'W', \
'BD', 5111]
    """
    return [str_to_date(row[0]), str_to_time(row[1]), row[2], row[3], row[4], int(row[5]), int(row[6]), row[7],
            row[8], int(row[9])]


def str_to_date(date_string: str) -> datetime.date:
    """Convert a string in mm/dd/yyyy format to a datetime.date.

    Hints:
    1. You can use str.split(date_string, '/') to first obtain
       the three strings corresponding to month, day, and year separately.
    2. Create a new datetime.date value by calling this type on three arguments:
       datetime.date(year, month, day).

    Preconditions:
    - date_string has format mm/dd/yyyy

    >>> str_to_date('01/01/2014')
    datetime.date(2014, 1, 1)
    """
    month, day, year = str.split(date_string, '/')
    return datetime.date(int(year), int(month), int(day))


def str_to_time(time_string: str) -> datetime.time:
    """Convert a time string with hours and minutes to a datetime.time.

    Preconditions:
    - time_string has format HH:mm, where the hours are specified in 24-hour format (from 00 to 23).

    Similar hint as str_to_date. datetime.time takes two arguments:
    hour and minute, in that order.

    >>> str_to_time('00:21')
    datetime.time(0, 21)
    """
    hour, minute = str.split(time_string, ':')
    return datetime.time(int(hour), int(minute))


###############################################################################
# Operating on the data
###############################################################################
def longest_delay(data: list[list]) -> int:
    """Return the longest delay in the given data.

    Notes:
    - As stated in the handout, you must use comprehensions and built-in functions, not for loops for this function.

    Preconditions:
    - data != []
    - data is in the format of the TTC subway delays csv file

    >>> delay_data = read_csv_file('twolines.csv')
    >>> longest_delay(delay_data[1])
    55
    """
    return max([this_data[5] for this_data in data])


def average_delay(data: list[list]) -> float:
    """Return the average subway delay in data.

    Notes:
    - As stated in the handout, you must use comprehensions and built-in functions, not for loops for this function.

    Preconditions:
    - data != []
    - data is in the format of the TTC subway delays csv file

    >>> delay_data = read_csv_file('twolines.csv')
    >>> average_delay(delay_data[1])
    29.0
    """
    return sum([this_data[5] for this_data in data]) / len(data)


def num_delays_by_month(data: list[list], year: int, month: int) -> int:
    """Return the number of delays that occurred in the given month and year.

    Notes:
    - As stated in the handout, you must use comprehensions and built-in functions, not for loops for this function.

    Preconditions:
    - data is in the format of the TTC subway delays csv file
    - 0 < month <= 12
    - 2014 <= year <= 2019

    >>> delay_data = read_csv_file('twolines.csv')
    >>> num_delays_by_month(delay_data[1], 2014, 1)
    2
    >>> num_delays_by_month(delay_data[1], 2014, 2)
    0
    """
    return len([delay for delay in data if delay[0].year == year and delay[0].month == month])


if __name__ == '__main__':
    # DO NOT MODIFY ANY CODE BELOW (You can and should comment/uncomment them out for testing purposes though)
    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['csv', 'datetime'],
        'allowed-io': ['read_csv_file'],
        'max-line-length': 120
    })
