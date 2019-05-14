import tensorflow as tf
from tensorflow import keras
import pandas as pd
import os
import sys
import ast

# 81 input neurons
# 2 output neurons

path = os.path.join(sys.path[0], 'GameFiles/gamestate2.csv')

df = pd.DataFrame.from_csv(path)

features = ['feature%d'%i for i in range(81)]

#dataset = tf.data.Dataset.from_tensor_slices((tf.cast(df[features].values, tf.int8),
#                                              tf.cast(df['labels'].values, tf.int8)))
#dataset.shuffle(25000)

model = keras.Sequential([
    keras.layers.Input(shape=(81,)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(2, activation='softmax')# Output layer
    ])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

model.fit(df[features][:15000], df['labels'][:15000], epochs=1)

model.evaluate(df[features][15000:], df['labels'][15000:])