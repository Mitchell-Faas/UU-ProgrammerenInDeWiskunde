# The quicksort code won't be commented, since it's a common algorithm.
from random import randint
def quicksort(list, left=0, right=-1):
    """Sorts a list L by using quicksort."""
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

difficulties = [int(x) for x in input().split()]
smartness = [int(x) for x in input().split()]
# Sort both inplace
quicksort(difficulties)
quicksort(smartness)

solvedtotal = True
for problem in difficulties:
    solved = False
    for idx, mathematician in enumerate(smartness):
        if problem < mathematician and problem >= mathematician/2:
            # Success!
            smartness[idx] = -1
            solved = True
            break
    if not solved:
        print("onmogelijk")
        solvedtotal = False
        break
else:
    if solvedtotal:
        print("mogelijk")
