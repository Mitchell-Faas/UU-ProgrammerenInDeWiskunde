
year = int(input())

# Basic rule
if (year % 4 == 0) and \
    ((year % 100 != 0) or (year % 400 == 0)):
    # Complicated  rule
    print("schrikkeljaar")
else:
    print("geen schrikkeljaar")