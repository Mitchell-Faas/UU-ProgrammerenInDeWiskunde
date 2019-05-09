from datetime import date

def is_leap_year(year):
    if (year % 4 == 0) and \
            ((year % 100 != 0) or (year % 400 == 0)):
        # Complicated  rule
        return True
    return False

while True:
    day, month, year = [int(x) for x in input("Input day/month/year:\n").split()]

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
    known = date(year, 4, 4) # 4th of april is always on the doomsday
    unknown = date(year, month, day)
    difference = (known - unknown).days

    diff_mod7 = difference % 7

    day = (doomsday + diff_mod7) % 7

    anchor_text = num_to_day[day]

    print(anchor_text)