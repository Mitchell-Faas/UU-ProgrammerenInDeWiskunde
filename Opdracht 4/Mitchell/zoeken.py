def bisectie_rec(list, target, left = 0, right = -1):
    if len(list) == 0:
        return -1

    if right == -1:
        right = len(list) - 1


    idx = rround((right+left) / 2)

    # Check middle
    if list[idx] == target:
        output = idx
    elif left == right: # We're on the same number, and it's not target, so doesn't exist.
        return -1
    elif list[idx] > target:
        output = bisectie_rec(list, target, left=left, right=idx)
    else: # list[idx] < target:
        output = bisectie_rec(list, target, left=idx, right=right)

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

def bisectie_it(list, target):
    if len(list) == 0:
        return -1

    left = 0
    right = len(list) - 1


    while True:
        idx = rround((right+left) / 2)

        # Check middle
        if list[idx] == target:
            output = idx
            break
        elif left == right: # We're on the same number, and it's not target, so doesn't exist.
            return -1
        elif list[idx] > target:
            right = idx
        else: # list[idx] < target:
            left = idx

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

def rround(x):
    if (x%1 == 0.5):
        return round(x) + 1
    else:
        return round(x)


if __name__ == '__main__':
    print(bisectie_it([1, 1] , 4))
