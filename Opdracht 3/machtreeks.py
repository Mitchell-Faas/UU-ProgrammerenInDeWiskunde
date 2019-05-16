from decimal import Decimal # Credit naar degene die dit heeft gemaakt \
# https://stackoverflow.com/questions/6913532/display-a-decimal-in-scientific-notation
temp = input().split(' ')
z = float(temp[0])
n = int(temp[1])
m = int(temp[2])

s = 0
for k in range(n,m+1):
    s += k * z**k

output = '%.2E' % Decimal(s)

print(output)