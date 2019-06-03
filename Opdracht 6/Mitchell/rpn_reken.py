from collections import deque
inputlist = input().split()

operands = deque()

for char in inputlist:
    # Precursive checking for int (Error raising is too slow)
    if char.isdigit():
        # Convert to number
        operands.append(int(char))
    else:
        # input is not convertible to number, so is an operation and the previous 2 are numbers
        b, a = operands.pop(), operands.pop()

        if char == '+':
            operands.append(a + b)
        if char == '-':
            operands.append(a - b)
        if char == '*':
            operands.append(a * b)
        if char == '/':
            operands.append(a / b)

print(float(operands.pop()))
