import os
import re

path = 'S:/sgf-files'

re_find_size = re.compile(r'[Ss][Zz]\[(.*?)\]')
re_wincondition = re.compile(r'[Rr][Ee]\[[BbWw](.*?)\]')



counter = 0

for dirpath, dirname, filenames in os.walk(path):
    for filename in filenames:
        filepath = os.path.join(dirpath, filename)

        try:
            with open(filepath, 'r') as file:
                file_string = file.read()

                size = int(re.search(re_find_size, file_string).group(1))
                wincondition = re.search(re_wincondition, file_string).group(1)

            if size != 9 and wincondition.upper() == '+T':
                os.remove(filepath)
                print('removed', filepath)

            print('go to next')
        except (UnicodeDecodeError, AttributeError, ValueError):
            os.remove(filepath)
            print('removed', filepath)
            continue

print(counter)