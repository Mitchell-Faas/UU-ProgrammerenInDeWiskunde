import random
from math import ceil, floor

def bisectie_rec(list, goal, startindex=0, endindex=-1):
    # Initially set endindex to last index in list
    if endindex == -1:
        endindex = len(list)-1
    # If goal is reached, return goal index
    if list[startindex] == goal:
        return startindex
    # If startindex and endindex have reached each other without finding the goal, return negative
    if endindex - startindex <= 1:
        if list[endindex] == goal:
            return endindex
        else:
            return -1
    middleindex = (startindex + endindex) // 2
    # Take the first half of the list if the goal is in there
    if list[middleindex] < goal:
        return bisectie_rec(list, goal, startindex=middleindex, endindex=endindex)
    # Take the second half of the list if the goal is in there
    elif list[middleindex] > goal:
        return bisectie_rec(list, goal, startindex=startindex, endindex=middleindex)
    # If the middle index is the goal, shift it to see if it is the first such goal
    if list[middleindex] == goal:
        return bisectie_rec(list, goal, startindex=startindex, endindex=endindex-1)

def bisectie_it(list, goal):
    startindex = 0
    endindex = len(list) - 1
    while list[startindex] != goal:
        # print(startindex, endindex, list[startindex], list[endindex], goal)
        middleindex = (startindex + endindex) // 2
        if list[middleindex] < goal:
            startindex = middleindex
        if list[middleindex] > goal:
            endindex = middleindex
        if list[middleindex] == goal:
            endindex -= 1
        if endindex - startindex <= 1:
            startindex += 1
        if endindex < startindex:
            return -1
    return startindex



"""randlen = 100
randsize = 100
randlist = [random.randint(1,randsize) for _ in range(randlen)]
randlist.sort()
print(randlist)
goal = random.randint(1,randsize)
print(bisectie_it(randlist, goal))"""