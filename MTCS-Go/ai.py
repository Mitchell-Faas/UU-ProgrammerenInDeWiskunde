import os
import sys

import pandas as pd

# 81 input neurons
# 2 output neurons

path = os.path.join(sys.path[0], 'GameFiles/gamestates.csv')

df = pd.DataFrame.from_csv(path)

print(df)