from seq2seq import SimpleSeq2Seq, Seq2Seq, AttentionSeq2Seq
import numpy as np
from keras.utils.test_utils import keras_test
from nn.preprocessing import divideData

input_length = 100
input_dim = 2

output_length = 100
output_dim = 1

samples = 100
hidden_dim = 24

def test_AttentionSeq2Seq():
    X_train, y_train, X_test, y_test, X_validation, y_validation = divideData('Database.txt', 100)
    models = [ ]
    models += [ AttentionSeq2Seq(output_dim=output_dim, hidden_dim=hidden_dim, output_length=output_length,
                                 input_shape=(input_length, input_dim)) ]
    models += [ AttentionSeq2Seq(output_dim=output_dim, hidden_dim=hidden_dim, output_length=output_length,
                                 input_shape=(input_length, input_dim), depth=2) ]
    models += [ AttentionSeq2Seq(output_dim=output_dim, hidden_dim=hidden_dim, output_length=output_length,
                                 input_shape=(input_length, input_dim), depth=3) ]

    for model in models:
        model.compile(loss='mse', optimizer='sgd')
        model.fit(x, y, epochs=1)
