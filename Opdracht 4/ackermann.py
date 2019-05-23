def a(m, n):
    if m == 0:
        return n+1
    else:
        if n == 0:
            return a(m-1, 1)
        else:
            return a(m-1, a(m, n-1))

m, n = [int(x) for x in input().split()]
print(a(m, n))