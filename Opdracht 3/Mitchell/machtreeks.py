import numpy as np

# Ask for input (z,n,m)
z, n, m = input().split()
# Convert to proper dtype
z, n, m = float(z), int(n), int(m)

# Create array to represent k in the sum
k_array = np.arange(n, m+1)

# Make array of every element in sum expansion, and sum it.
sum = np.sum(k_array * (z**k_array))

# Convert to scientific and print.
print(np.format_float_scientific(sum, precision=2, unique=False))
