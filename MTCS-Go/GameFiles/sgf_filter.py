import sys
import re
import os

print(sys.path[0])


path = ""

re_size_find = re.compile(r'SZ\[(..)\]')

with open(path, 'r') as file:
    game = file.read()

    size = int(re.search(re_size_find, game).group(1))

if size != 9:
    os.remove(path)
