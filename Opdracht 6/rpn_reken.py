inputlist = input().split()

operands = []

for char in inputlist:
    # Precursive checking for int (Error raising is too slow)
    if char.isdigit():
        # Convert to number
        operands.append(int(char))
    else:
        # input is not convertible to number, so is an operation and the previous 2 are numbers
        if char == '+':
            operands.append(operands.pop() + operands.pop())
        if char == '-':
            operands.append(operands.pop() + operands.pop())
        if char == '*':
            operands.append(operands.pop() + operands.pop())
        if char == '/':
            operands.append(operands.pop() + operands.pop())

print(float(operands.pop()))
