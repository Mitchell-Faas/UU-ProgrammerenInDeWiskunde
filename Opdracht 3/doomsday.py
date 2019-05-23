#!/usr/bin/env python3
import sys

def date_to_weekday(date_list):
    day, month, year = [int(x) for x in date_list]
    is_leap_year = (not year % 4 and year % 100) or year % 400
    if month == 1:
        if is_leap_year:
            anchor = 4
        else:
            anchor = 3
    elif month == 2:
        if is_leap_year:
            anchor = 29
        else:
            anchor = 28
    elif month == 3:
        anchor = 0
    elif month == 4:
        anchor = 4
    elif month == 5:
        anchor = 9
    elif month == 6:
        anchor = 6
    elif month == 7:
        anchor = 11
    elif month == 8:
        anchor = 8
    elif month == 9:
        anchor = 5
    elif month == 10:
        anchor = 10
    elif month == 11:
        anchor = 7
    elif month == 12:
        anchor = 12

    weekday_int = (doomsday(year) + (day - anchor)) % 7
    weekdayDict = {'0': 'sunday', '1':'monday', '2':'tuesday', '3':'wednesday',
                   '4':'thursday', '5':'friday', '6':'saturday'}
    output = weekdayDict[str(weekday_int)]
    return(output)



def doomsday(year):
    # Using the "odd+11" formula from https://en.wikipedia.org/wiki/Doomsday_rule
    T = year % 100
    common_value = int(0.5 * (T + 11 * (T % 2)))
    offset = 7 - (( common_value + 11 * (common_value % 2) ) % 7 )

    century = int(year/100) * 100 # Rounds down to century
    if century % 400 == 200:
        century_anchor = 5
    elif century % 400 == 300:
        century_anchor = 3
    elif century % 400 == 0:
        century_anchor = 2
    elif century % 400 == 100:
        century_anchor = 0

    output = (century_anchor + offset) % 7
    return output

print(date_to_weekday(sys.argv[1:]))
