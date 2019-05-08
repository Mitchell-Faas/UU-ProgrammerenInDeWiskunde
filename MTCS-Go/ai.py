import tensorflow as tf
from tensorflow import keras
import pandas as pd
import os
import sys
import ast

# 81 input neurons
# 2 output neurons

path = os.path.join(sys.path[0], 'GameFiles/gamestates2.csv')
print(path)

df = pd.DataFrame.from_csv(path)
df['features'] = df["features"].apply(ast.literal_eval)
print(type(df['features'][5]))
df2 = pd.DataFrame(df['features'].tolist(), columns=['feature%d'%i for i in range(81)])
df2['labels'] = df['labels']

df2.to_csv(os.path.join(sys.path[0], 'gamestate2.csv'))
print(df2)