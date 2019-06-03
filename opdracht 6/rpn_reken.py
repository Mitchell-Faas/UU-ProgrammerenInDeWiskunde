
def revpolish(inputstring):
    commandstring = inputstring.split()
    stack = []
    for command in commandstring:
        if command == '+':
            b = stack.pop()
            a = stack.pop()
            stack.append(a+b)
        elif command == '-':
            b = stack.pop()
            a = stack.pop()
            stack.append(a-b)
        elif command == '/':
            b = stack.pop()
            a = stack.pop()
            stack.append(a/b)
        elif command == '*':
            b = stack.pop()
            a = stack.pop()
            stack.append(a*b)
        else:
            stack.append(int(command))

    return(float(stack[0]))

inputstring = input()
print(revpolish(inputstring))