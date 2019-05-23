def bisectie_rec2(list, target, left = 0, right = -1):
    if len(list) == 0:
        return -1

    if right == -1:
        right = len(list) - 1

    middle = (right+left) // 2

    # Check middle
    if list[middle] == target:
        output = middle
    elif list[middle] > target:
        output = bisectie_rec(list, target, left=left, right=middle-1)
    else: # list[idx] < target:
        output = bisectie_rec(list, target, left=middle+1, right=right)

    # We need the left most idx, so we'll walk left until we're done
    try:
        while True:
            if list[output-1] != list[output] or output == 0:
                break
            else:
                output -= 1
    except IndexError:
        pass

    return output

def bisectie_it2(list, target):
    if len(list) == 0:
        return -1

    left = 0
    right = len(list) - 1
    output = -1

    while left <= right:
        idx = (right+left) // 2
        # Check middle
        if list[idx] == target:
            output = idx
            break
        elif list[idx] > target:
            right = idx-1
        else: # list[idx] < target:
            left = idx+1
    else:
        # If output hasn't changed, then the element doesn't exist.
        if output == -1:
            return -1

    # We need the left most idx, so we'll walk left until we're done
    try:
        while True:
            if list[output-1] != list[output] or output == 0:
                break
            else:
                output -= 1
    except IndexError:
        pass

    return output
