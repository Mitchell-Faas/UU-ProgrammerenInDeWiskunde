def pascal(i, j):

    # If we're on the edge, we return 1
    if j == 0 or j == i:
        return 1

    # Start recursion
    pascal_ij = pascal(i-1, j) + pascal(i-1, j-1)

    return pascal_ij

if __name__ == '__main__':
    k, n = [int(x) for x in input().split()]
    print(pascal(n-1, k-1))
