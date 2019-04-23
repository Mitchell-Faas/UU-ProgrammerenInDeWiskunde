import numpy as np

arr = np.array([x.__len__() for x in input().split(sep=' ')])

print(np.sum(arr), np.product(arr))