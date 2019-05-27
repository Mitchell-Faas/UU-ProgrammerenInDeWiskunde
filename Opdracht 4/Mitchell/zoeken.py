def bisectie_rec(arr, x, l=0, r=-1):
    if r == -1:
        r = len(arr) - 1

    # Check base case
    if r >= l:

        mid = l + (r - l) / 2

        # If element is present at the middle itself
        if arr[mid] == x:
            return mid

            # If element is smaller than mid, then it
        # can only be present in left subarray
        elif arr[mid] > x:
            return bisectie_rec(arr, l, mid - 1, x)

            # Else the element can only be present
        # in right subarray
        else:
            return bisectie_rec(arr, mid + 1, r, x)

    else:
        # Element is not present in the array
        return -1

def bisectie_it(arr, x):
    if len(arr) == 0:
        return -1

    l = 0
    r = len(arr) - 1
    while l <= r:

        mid = l + (r - l) / 2;

        # Check if x is present at mid
        if arr[mid] == x:
            return mid

            # If x is greater, ignore left half
        elif arr[mid] < x:
            l = mid + 1

        # If x is smaller, ignore right half
        else:
            r = mid - 1

    # If we reach here, then the element
    # was not present
    return -1


if __name__ == '__main__':
    print(bisectie_it([], 1))
