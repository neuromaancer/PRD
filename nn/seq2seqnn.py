from seq2seq.models import AttentionSeq2Seq
import numpy as np
from keras.callbacks import LearningRateScheduler
from keras.utils.np_utils import to_categorical
import keras.backend as K
from nn.preprocessing import divideData

input_length = 100
input_dim = 2

output_length = 100
output_dim = 1

samples = 100
hidden_dim = 24


def Seq2SeqModel():
    X_train, y_train, X_test, y_test, X_validation, y_validation = divideData('Database.txt', 100)
    # print(y_train)

    models = [ ]
    models += [ AttentionSeq2Seq(output_dim=output_dim, hidden_dim=hidden_dim, output_length=output_length,
                                 input_shape=(input_length, input_dim)) ]
    models += [ AttentionSeq2Seq(output_dim=output_dim, hidden_dim=hidden_dim, output_length=output_length,
                                 input_shape=(input_length, input_dim), depth=2) ]
    models += [ AttentionSeq2Seq(output_dim=output_dim, hidden_dim=hidden_dim, output_length=output_length,
                                 input_shape=(input_length, input_dim), depth=3) ]

    for model in models:
        model.compile(loss='mse', optimizer='adadelta', metrics=[ 'accuracy' ])
        # YY = [ ]
        # for y in y_train:
        #     print(to_categorical(y)[1])
        #     YY.append(to_categorical(y))
        #
        # YY = np.asarray(YY)
        # print(YY.shape)
        model.fit(X_train, y_train, epochs=1)
        predict_test = model.predict(X_test)
        predict = K.argmax(predict_test, axis=1)
        print(predict_test[ 0 ][ 43 ])
        print(predict_test[ 0 ][ 1 ])
        print("------")
        print(y_test[ 0 ][ 43 ])
        print(y_test[ 0 ][ 1 ])


if __name__ == '__main__':
    Seq2SeqModel()
