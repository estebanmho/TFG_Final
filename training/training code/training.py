import tensorflow as tf
import numpy as np
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

i = 0
def one_hot(d):  # codificación one_hot
    num_classes = len(set(d))
    rows = d.shape[0]
    labels = np.zeros((rows, num_classes), dtype='float32')
    labels[np.arange(rows), d.T - 1] = 1
    return labels


class PeriodicPrint(tf.keras.callbacks.Callback):
    def __init__(self, period=100):
        self.trace = period

    def on_epoch_end(self, epoch, logs=None):  # es llamado cada vez que termina un epoch
        if (epoch + 1) % self.trace == 0:
            print(f"epoch: {epoch + 1}; loss: {logs['loss']:.5f}; accuracy: {logs['accuracy']:.5f}; MAE: {logs['mean_absolute_error']:.5f}; MSE: {logs['mean_squared_error']:.5f}")
            if epoch == 1699:
                global i
                i = float(logs['accuracy'])

X = np.loadtxt('../data/shuffle_simb_valido.csv', delimiter=",", dtype='float64', usecols=range(1,7), skiprows=1)
L = np.loadtxt('../data/shuffle_simb_valido.csv', delimiter=",", dtype='int', usecols=[7], skiprows=1)

d = np.array(L)
X = np.array(X)
d = one_hot(d)
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(4, activation='relu', input_shape=(X.shape[1],)))
model.add(tf.keras.layers.Dense(8, activation='relu'))
model.add(tf.keras.layers.Dropout(0.1))
model.add(tf.keras.layers.Dense(11, activation='relu'))
#model.add(tf.keras.layers.Dense(5, activation='relu'))
model.add(tf.keras.layers.Dropout(0.15))
model.add(tf.keras.layers.Dense(8, activation='relu'))
#model.add(tf.keras.layers.Dense(5, activation='relu'))
model.add(tf.keras.layers.Dropout(0.1))
model.add(tf.keras.layers.Dense(d.shape[1], activation='softmax'))
model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['mean_absolute_error', 'mean_squared_error', 'accuracy'])

print('training...')
h = model.fit(X, d, epochs=1700, verbose=0, callbacks=[PeriodicPrint(100)])
print('trained')
if i > 0.90:
    model.save('../models/simb_valido.h5')

