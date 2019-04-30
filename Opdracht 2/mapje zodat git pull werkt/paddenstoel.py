def lekkerofniet(x0, x1, x2):
    if x0 < 0.5:
        return 1

    if x1 < 0.3 or x1 > 0.7:
        return 2

    if x2 < 1/3:
        return 3
    elif 1/3 <= x2 < 2/3:
        return 4
    else:
        return 5

#proplist = [float(x) for x in input().split(',')]
#x0, x1, x2 = proplist
#lekkerofniet(x0,x1,x2)