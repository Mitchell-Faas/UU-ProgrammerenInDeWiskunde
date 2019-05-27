tree_list = [int(x) for x in input().split()]
move_sequence = input()

# Figure out the amount of steps
length = len(tree_list)
h = len(move_sequence)
while True:
    if 2**(h+1) -1 == length:
        break
    h += 1

class Tree():
    def __init__(self):
        self.left = None
        self.right = None
        self.data = None



