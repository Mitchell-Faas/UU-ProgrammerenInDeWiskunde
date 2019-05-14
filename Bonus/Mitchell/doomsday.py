#!/usr/bin/env python3
from datetime import date
import sys

def is_leap_year(year):
    if (year % 4 == 0) and \
            ((year % 100 != 0) or (year % 400 == 0)):
        # Complicated  rule
        return True
    return False

def day_difference(date1, date2, year):
    """Calculates date1 - date2"""
    day1, month1 = date1
    day2, month2 = date2

    length_dict = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30,
                   7:31, 8:31, 9:30, 10:31, 11:30, 12:31}

    if is_leap_year(year):
        length_dict[2] += 1

    if month1 == month2:
        return day1 - day2
    if month1 > month2:
        sum = 0
        while month1 > month2:
            sum += day1
            month1 -= 1
            day1 = length_dict[month1]
        sum += (day1 - day2)
        return sum
    if month1 < month2:
        sum = 0
        while month1 < month2:
            sum -= length_dict[month1] - day1
            day1 = 0
            month1 += 1
        sum -= day2
        return sum




def doomsday(intlist):
    day, month, year = intlist

    num_to_day = {0: 'sunday', 1: 'monday', 2: 'tuesday', 3: 'wednesday',
                  4: 'thursday', 5: 'friday', 6: 'saturday'}

    # Find century's anchor day
    century = year // 100
    century_anchor = 5 * (century % 4) % 7 + 2

    # Find year's doomsday
    last_2_digits = year % 100

    doomsday_plus = (last_2_digits + (last_2_digits // 4)) % 7

    doomsday = (century_anchor + doomsday_plus) % 7

    # Days between known and unknown
#    known = date(year, 4, 4) # 4th of april is always on the doomsday
#    unknown = date(year, month, day)
#    difference = (unknown - known).days
#    print(difference)

    difference = day_difference((day, month), (4, 4), year)

    diff_mod7 = difference % 7

    day = (doomsday + diff_mod7) % 7

    anchor_text = num_to_day[day]

    print(anchor_text)

try:
    doomsday([int(x) for x in sys.argv[1:]])
except ValueError:
    doomsday([int(x) for x in input().split()])