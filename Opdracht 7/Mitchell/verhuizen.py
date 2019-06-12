import numpy as np

# Get input
family_members = np.array([int(x) for x in input().split()])

# Partition family_members through introselect (modified quickselect with worstcase O(nlog(n))
# Expected O(n)
half = len(family_members) // 2
family_members.partition(kth=half)

# O(n)
max_left = np.max(family_members[:half])
min_right = np.min(family_members[half:])

# Take average of max_left and min_right
henk = (max_left + min_right) // 2

# Calculate distance
# O(n)
distance = np.sum(np.abs(family_members-henk))

print(distance)