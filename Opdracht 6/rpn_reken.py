inputlist = input().split()

idx = 0
while True:
    try:
        try:  # If input is convertible to number, do so.
            inputlist[idx] = int(inputlist[idx])
            idx += 1
        except ValueError:
            # input is not convertible to number, so is an operation and the previous 2 are numbers
            if inputlist[idx] == '+':
                inputlist[idx] = inputlist[idx-2] + inputlist[idx-1]
            if inputlist[idx] == '-':
                inputlist[idx] = inputlist[idx-2] - inputlist[idx-1]
            if inputlist[idx] == '*':
                inputlist[idx] = inputlist[idx-2] * inputlist[idx-1]
            if inputlist[idx] == '/':
                inputlist[idx] = inputlist[idx-2] / inputlist[idx-1]

            # Remove the 2 old values (Order is important here)
            del inputlist[idx - 1]
            del inputlist[idx - 2]

            idx -= 1
    except IndexError:
        break

print(float(inputlist[0]))