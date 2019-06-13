import numpy as np

# Get first line
n = int(input())

coefficient_matrix = []
for _ in range(n):
    coefficient_matrix.append([int(x) for x in input().split()])

# Grab p
p = int(input())

def mod_inverse(x):
    """Calculates the inverse mod p because
    x^(p-1) = 1 (mod p) - Fermat's little theorem"""
    return pow(x, p-2, p)

tempeq = coefficient_matrix[-1]
for i in range(n-1):
    tempeq -= coefficient_matrix[i]

X = mod_inverse(tempeq[0])
a = (tempeq[-1]*X)%p






# Turn in to np.array()
coefficient_matrix = np.array(coefficient_matrix)

# Split in to results and coefficient matrix
coefficient_matrix, result_vector = coefficient_matrix[:,:-1], coefficient_matrix[:, -1]



# Add another column
p_vector = np.ones((n, n+1))*p
coefficient_matrix = np.append(coefficient_matrix, p_vector, axis=1)


print(np.linalg.lstsq(coefficient_matrix, result_vector))