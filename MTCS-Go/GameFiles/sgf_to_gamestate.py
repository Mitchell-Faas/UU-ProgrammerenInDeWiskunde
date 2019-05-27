from goban.goban import *
import pandas as pd
import sys
import os
import re

# Get folder path
folder_path = 'S:/sgf-files'

# Define move regex
re_move_find = re.compile(r'([WB])\[(..)\]')
re_find_result = re.compile(r'[Rr][Ee]\[([BbWw]).*?\]')

# List every file
folder = os.listdir(folder_path)

def char_to_int(char):
    """Takes in an alphabetical character, and outputs
    its 0-indexed location in the alphabet.
    Example: a->0, c->2, z->25"""
    return ord(char.lower()) - ord('a')

data = {'features': [], 'labels': []}

for dirpath, dirname, filenames in os.walk(folder_path):
    for filename in filenames:
        filepath = os.path.join(dirpath, filename)
        # Initialize the go board. We know size = 9
        board = GoBoard(board_size=9)

        win = '1'  # 1 == white, 0 == black

        # Open file
        with open(filepath, 'r') as game:
            file_string = game.read()

            # Find winner
            winner = re.search(re_find_result, file_string).group(1)

            # Select value for label column
            if winner.upper() == 'W':
                win = 1
            elif winner.upper() == 'B':
                win = 0
            else:
                raise ValueError("weird winner in file %s"%filepath)


            # Find features
            list = re.findall(re_move_find, file_string)
            # append stuff
            for move in list:
                color = move[0].lower()  # Have to make sure it's lower case
                x = char_to_int(move[1][0])
                y = char_to_int(move[1][1])

                try:
                    # Make move on GoBoard
                    board.apply_move(color, (x, y))
                except ValueError:
                    # Move is illegal
                    continue

                # Append data to dict
                data['features'].append(to_list(board))
                data['labels'].append(win)

print(len(data['features'][1]))

df = pd.DataFrame(data)
df.to_csv(os.path.join(sys.path[0], 'gamestates.csv'))