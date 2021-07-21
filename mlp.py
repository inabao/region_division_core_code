import tensorflow as tf
from tensorflow import keras
import copy
import numpy as np
import matplotlib.pyplot as plt
from data_deal import order_distribution


n = 16
l = 8

day = 1
t = 0
m = 0
train_x = []
train_y = []
tmp_x = []
while day < 31:
    t_later = (t + (m + 30) // 60)
    m_later = (m + 30) // 60
    z = order_distribution(day, depart=(n, n), start=(t,m), end=(t_later, m_later))
    if t_later == 24:
        t_later = 0
        day += 1
    t = t_later
    m = m_later
    if len(tmp_x) == 8:
        train_x.append(tmp_x)
        train_y.append(z)
        tmp_x.pop(0)
    tmp_x.append(z)

train_x = np.array(train_x)
train_y = np.array(train_y)
train_x, test_x = train_x[:int(len(train_x) * 0.8)], train_x[int(len(train_x) * 0.8):]
train_y, test_y = train_y[:int(len(train_y) * 0.8)], train_y[int(len(train_y) * 0.8):]
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(8, n, n)),
    keras.layers.Dense(128, activation='tanh'),
    keras.layers.Dense(n*n)
])

model.compile(optimizer="adam", loss="mse", metrics=["mae"])


model.fit(train_x, train_y, epochs=100, validation_split=0.3)
loss, acc = model.evaluate(test_x, test_y)
print(acc)