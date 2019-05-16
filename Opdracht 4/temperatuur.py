templist = [int(x) for x in input().split()]
maxtemp = templist[0]
maxdiff = 0
for temp in templist:
    maxtemp = max(temp, maxtemp)
    maxdiff = max(maxtemp - temp, maxdiff)

print(maxdiff)