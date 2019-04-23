import math
n, R = [float(x) for x in input().split()]
volume = (math.pow(math.pi, n/2)/math.factorial(n/2))*math.pow(R,n)
print(round(volume,2))