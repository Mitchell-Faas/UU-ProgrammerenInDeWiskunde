# The quicksort code won't be commented, since it's a common algorithm.
from random import randint
from time import time_ns as time
def quicksort(list, left=0, right=-1):
    """Sorts a list L by using quicksort. Fails for lists that have more than
    1000 elements of the same value."""
    if right == -1:
        right = len(list) - 1

    idx = split(list, left, right)
    if idx-1 > left:
        quicksort(list, left, idx-1)
    if idx+1 < right:
        quicksort(list, idx+1, right)

def split(list, left, right):
    pivot = randint(left, right)
    comparison = list[pivot]
    list[pivot], list[right] = list[right], list[pivot]

    idx = left
    for j in range(left, right):
        if list[j] < comparison:
            list[idx], list[j] = list[j], list[idx]
            idx += 1

    list[idx], list[right] = list[right], list[idx]

    return idx
'''
difficulties = [int(x) for x in input().split()]
smartness = [int(x) for x in input().split()]
# Sort both inplace
quicksort(difficulties)
quicksort(smartness)

solved = True
for idx, problem in enumerate(difficulties):
    if not (problem <= smartness[idx] and problem >= smartness[idx]/2):
        # Fail :(
        solved = False
        break
if solved:
    print("mogelijk")
else:
    print("onmogelijk")
'''
times = []
for exp in range(25):
    try:
        randlist = [randint(0, 1000) for x in range(2 ** exp)]
        tic = time()
        quicksort(randlist)
        toc = time()
        times.append(toc-tic)
        print("Finished size", 2**exp, "in", (toc-tic)/10**9, "seconds.")
    except RecursionError:
        print("Reached recursion depth.")
        pass

print(times)