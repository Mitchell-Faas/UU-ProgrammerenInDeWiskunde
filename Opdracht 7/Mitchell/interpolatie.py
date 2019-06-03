# Get the input
in_set = [int(x) for x in input().split()]

# We need a minimum of 3 elements to be able to do this.
# This figures out the step size
step_size = min(in_set[1]-in_set[0], in_set[2]-in_set[1])

# Knowing the step size, we can use a binary search
left = 0
right = len(in_set) - 1
middle = None
while left + 1 != right:
    # Find middle
    middle = (left+right) // 2

    # If the left sequence is good
    if (in_set[middle] - in_set[left]) == (middle-left)*step_size:
        # Move to the right side
        left = middle
        continue
    else:
        # Stay in the left side
        right = middle
        continue

# While has terminated, so we know that left+1 = right, and that the jump happens between them.
# Therefore we can increment one stepsize to the left index.
print(left, in_set[left]+step_size)
