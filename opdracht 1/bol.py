import math
n, R = [int(x) for x in input().split()]
volume = (math.pow(math.pi, n/2)/math.factorial(n/2))*math.pow(R,n)
print(volume)