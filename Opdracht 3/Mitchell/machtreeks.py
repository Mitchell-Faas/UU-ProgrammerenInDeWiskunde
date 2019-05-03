def de_python_manier(z, n, m):
    # time for 1mil iterations (z, n, m) = (0.999, 5, 1000)
    # is 40.62 sec
    import numpy as np
    # Create array to represent k in the sum
    k_array = np.arange(n, m + 1)

    # Make array of every element in sum expansion, and sum it.
    sum = np.sum(k_array * (z ** k_array))

    # Convert to scientific notation.
    return np.format_float_scientific(sum, precision=2, unique=False)

def de_C_manier(z, n, m):
    # time for 1mil iterations (z, n, m) = (0.999, 5, 1000)
    # is 223.82 sec (5.5x the python way)
    from decimal import Decimal
    sum = 0
    for k in range(n, m+1):
        sum += k * (z ** k)

    # Convert the string
    return '%.2E' % Decimal(sum)

# Ask for input (z,n,m)
z, n, m = input().split()
# Convert to proper dtype
z, n, m = float(z), int(n), int(m)

print(de_C_manier(z, n, m))
