
line1 = [int(x) for x in input().split()]
line2 = [int(x) for x in input().split()]
line3 = [int(x) for x in input().split()]
line4 = [int(x) for x in input().split()]

"""
line1 = [0,0,0,0]
line2 = [1,0,0,3]
line3 = [4,0,0,2]
line4 = [0,0,0,0]
"""
inputsudoku = [line1, line2, line3, line4]


def sudo_solve(inputsudoku):
    # In this stack we will keep track of squares that have been filled but whose effect
    # on the possibilities of other quares still needs to be taken into account
    wipe_stack = []

    # A grid containing possible entries for each square
    possgrid = [[[1,2,3,4] for x in range(4)]for y in range(4)]
    # A grid keeping track of what squares have been used to wipe others and are therefore useless
    wipedgrid= [[False for x in range(4)]for y in range(4)]

    # A stack for previous grid-states to revert back to if a guess fails
    prev_grid_stack = []

    # A dictionary to tell us what square is diagonally opposite to another within the same quadrant
    diag_square_dict = {0:1,1:0,2:3,3:2}

    # We adjust the grid of possibilities based on the input sudoku
    for rowidx in range(4):
        for colidx in range(4):
            if inputsudoku[rowidx][colidx] != 0:
                wipe_stack.append((rowidx, colidx, inputsudoku[rowidx][colidx]))

    is_solved = False # Sudoku starts out unsolved
    not_direct_solvable = False # Start trying to solve directly

    while not is_solved: # While sudoku is unfinished
        if wipe_stack:
            wiperow, wipecol, wipeval = wipe_stack.pop()
            # Wipe vertical column
            for rowidx in range(4):
                try:
                    possgrid[rowidx][wipecol].remove(wipeval)
                except:
                    pass
            # Wipe horizontal row
            for colidx in range(4):
                try:
                    possgrid[wiperow][colidx].remove(wipeval)
                except:
                    pass

            # To wipe the quadrant we only need to wipe the diagonal square in it
            # The others we have already had
            diag_square_row = diag_square_dict[wiperow]
            diag_square_col = diag_square_dict[wipecol]
            try:
                possgrid[diag_square_row][diag_square_col]
            except:
                pass

            # We wiped the value from the square itself too, so we restore it
            possgrid[wiperow][wipecol] = [wipeval]
            # We take note that this square has reached its final value
            wipedgrid[wiperow][wipecol] = True


        else:
            # If each square has been set, the sudoku is complete
            if wipedgrid == [[True for x in range(4)]for y in range(4)]:
                is_solved = True
            else:
                # If the function passes here again without finding more squares to wipe, check:
                # Is there any mistake? If yes, revert the grid.
                # If no, make a guess.
                if not_direct_solvable:
                    mistake_was_made = False
                    for rowidx in range(4):
                        for colidx in range(4):
                            # If a square has no legal value we know we've made a mistake
                            if possgrid[rowidx][colidx] == []:
                                possgrid, wipedgrid = prev_grid_stack.pop()
                                mistake_was_made = True

                    # If the sudoku is not directly solvable, but there is no mistake, we need to guess
                    if not mistake_was_made:
                        guess_was_made = False
                        # Look if theres a square with only two possibilities first, otherwise three, etc
                        poss_len = 2
                        while not guess_was_made:
                            for rowidx in range(4):
                                for colidx in range(4):
                                    if len(possgrid[rowidx][colidx]) == poss_len:
                                        guess = possgrid[rowidx][colidx][0]
                                        guessrow = rowidx
                                        guesscol = colidx
                                        guess_was_made = True
                            poss_len += 1
                        prevpossgrid = possgrid.copy()
                        # If our guess turns out wrong and we revert back, we want that guess gone from the possgrid
                        prevpossgrid[guessrow][guesscol].remove(guess)
                        prevwipedgrid = wipedgrid.copy()
                        # Put them in the prev state stack for safekeeping
                        prev_grid_stack.append((prevpossgrid,prevwipedgrid))



                not_direct_solvable = True
                # Check for squares with only one possibility that haven't been used to wipe yet
                for rowidx in range(4):
                    for colidx in range(4):
                        if wipedgrid[rowidx][colidx] == False and len(possgrid[rowidx][colidx]) == 1:
                            wipe_stack.append((rowidx, colidx, possgrid[rowidx][colidx][0]))
                            not_direct_solvable = False

    return possgrid

solution = sudo_solve(inputsudoku)

for rowidx in range(4):
    row = [x for  x in solution[rowidx]]
    print(row[0][0],row[1][0],row[2][0],row[3][0])
