def wortel(a,epsilon):
    x = a

    for k in range(100):
        x = .5 * (x + a/x)
        if abs(x**2 - a) < epsilon:
            break

    return x