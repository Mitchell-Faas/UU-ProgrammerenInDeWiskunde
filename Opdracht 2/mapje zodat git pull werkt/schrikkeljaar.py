jaar = int(input())
if (jaar % 4 == 0 and jaar % 100 != 0) or jaar % 400 == 0:
    print('schrikkeljaar')
else:
    print('geen schrikkeljaar')