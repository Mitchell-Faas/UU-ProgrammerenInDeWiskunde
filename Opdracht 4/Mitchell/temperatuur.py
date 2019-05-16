templist = [int(x) for x in input().split()]

maxtemp, maxdrop = templist[0], 0
for temp in templist:
    maxtemp = max(maxtemp, temp)
    maxdrop = max(maxdrop, maxtemp - temp)

print(maxdrop)