def wortel(a, epsilon):
    x = a

    k = 0
    while abs(x**2-a)>=epsilon:
        k += 1
        x = (x + a*x**(-1)) / 2

        if k == 100:
            break

    return x



if __name__ == '__main__':
    a, epsilon = input().split()
    a, epsilon = int(a), float(epsilon)

    print(wortel(a, epsilon))