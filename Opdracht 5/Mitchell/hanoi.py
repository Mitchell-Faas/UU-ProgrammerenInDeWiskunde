# This recursion works because disk n can be considered as non-existent.
def hanoi_recursief(n, moveList, start='A', mid='B', end='C'):
    if n == 1:
        moveList.append(start + end)
        return

    # Put n-1 disks on the middle tower
    hanoi_recursief(n-1, moveList, start=start, mid=end, end=mid)
    # Put large disk on last tower
    moveList.append(start + end)
    # Put the n-1 disks on the last tower
    hanoi_recursief(n-1, moveList, start=mid, mid=start, end=end)

def hanoi_itteratief(n, moveList = -1):
    # Based on the restrictive algorithm found here:
    # https://en.wikipedia.org/wiki/Tower_of_Hanoi#Equivalent_iterative_solution
    def move(from_name, to_name):
        """Moves a stone from the from_name list, to the to_name list."""
        # Only two arguments are needed. Because this is a private function, we can assume
        # tower_dict and moveList to be reachable as planned.
        tower_dict[to_name].append(tower_dict[from_name].pop())
        moveList.append(from_name+to_name)

    if moveList == -1:
        moveList = []

    start, mid, end = 'A', 'B', 'C'
    # Initializes stacks. Note how a larger number signifies a smaller disk.
    tower_dict = {start: [x for x in range(n)], mid: [], end: []}
    # Total number of moves is known.
    total_moves = 2**n - 1

    last_moved = None

    # Make the first move
    if n%2 == 0:
        move(start, mid)
    else:
        move(start, end)

    # Make all the other moves
    for i in range(1, total_moves):
        # List all legal moves
        legal_list = [(start, mid), (start, end), (mid, start), (mid, end), (end, start), (end, mid)]

        to_discard = []

        # Discard any bad moves
        for from_name, to_name in legal_list:
            from_stack = tower_dict[from_name]
            to_stack = tower_dict[to_name]

            # If the from_stack is empty, then we don't care at all
            if from_stack == []:
                to_discard.append((from_name, to_name))
                continue
            from_disk = from_stack[-1]
            # If the to_stack is empty, then any number can go there
            if to_stack == []:
                to_disk = -1
            else:
                to_disk = to_stack[-1]

            # If the from disk is larger than the to disk, discard
            if from_disk < to_disk:
                to_discard.append((from_name, to_name))
                continue

            # No even/odd disk might be placed on another
            try:
                if from_disk%2 == to_disk%2 and not to_disk == -1:
                    to_discard.append((from_name, to_name))
                    continue
            except IndexError:
                pass

            # Never move a disk twice in succession
            if from_disk == last_moved:
                to_discard.append((from_name, to_name))
                continue

        for tup in to_discard:
            legal_list.remove(tup)

        # If there are 2 options, place on the option which has a disk
        if len(legal_list) == 2:
            if len(tower_dict[legal_list[0][1]]) == 0:
                # legal_list[0] is a movement to an empty tower
                del legal_list[0]

        # Length of legal_list is now 1.
        last_moved = tower_dict[legal_list[0][0]][-1]
        move(*legal_list[0])


    return moveList


if __name__ == '__main__':
    n = int(input())
    print(",".join(hanoi_itteratief(n)))