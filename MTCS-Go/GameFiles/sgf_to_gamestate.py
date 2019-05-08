from goban.goban import *
import pandas as pd
import sys
import os
import re

# Get folder path
folder_path = os.path.join(sys.path[0], "sgf-files\\")

# Define move regex
re_move_find = re.compile(r'([WB])\[(..)\]')

# List every file
folder = os.listdir(folder_path)

def char_to_int(char):
    """Takes in an alphabetical character, and outputs
    its 0-indexed location in the alphabet.
    Example: a->0, c->2, z->25"""
    return ord(char.lower()) - ord('a')

data = {'features': [], 'labels': []}

for sgf_file in folder:
    # Initialize the go board. We know size = 9
    board = GoBoard(board_size=9)

    win = '1' # 1 == white, 0 == black


    with open(os.path.join(folder_path, sgf_file), 'r') as game:
        for line in game:
            # Find the "result" line and change win dependent on it.
            if line[:2] == "RE":
                if line[3] == 'W':
                    win = 1
                elif line[3] == 'B':
                    win = 0

            # If the line is a line with moves
            elif line[:2] == ';B':
                list = re.findall(re_move_find, line)

                for move in list:
                    color = move[0].lower() # Have to make sure it's lower case
                    x = char_to_int(move[1][0])
                    y = char_to_int(move[1][1])

                    # Make move on GoBoard
                    board.apply_move(color, (x,y))

                    # Append data to dict
                    data['features'].append(to_list(board))
                    data['labels'].append(win)


print(len(data['features'][1]))

df = pd.DataFrame(data)
df.to_csv(os.path.join(sys.path[0], 'gamestates.csv'))