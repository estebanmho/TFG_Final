import tensorflow as tf
import numpy as np


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
            print(f"epoch: {epoch + 1}; loss: {logs['loss']:.5f}; accuracy: {logs['accuracy']:.5f}")


X = np.loadtxt('../data/simb_valido_test_santi.csv', delimiter=",", dtype='float64', usecols=range(0,6), skiprows=1)
L = np.loadtxt('../data/simb_valido_test_santi.csv', delimiter=",", dtype='int', usecols=[6], skiprows=1)

d = np.array(L)
X = np.array(X)
d = one_hot(d)
test_model = tf.keras.models.load_model('../models/simb_valido.h5')

test_model.evaluate(X, d, batch_size=30)