from seq2seq.models import AttentionSeq2Seq
import numpy as np

np.random.seed(1)

from keras.callbacks import LearningRateScheduler
from keras.utils.np_utils import to_categorical
import keras.backend as K
from nn.preprocessing import divideData, divideDataByIns
import matplotlib.pyplot as plt
from keras import layers
from keras.callbacks import ModelCheckpoint

input_length = 100
input_dim = 2

output_length = 100
output_dim = 2

samples = 100
hidden_dim = 100


def WinAcc(y_true, y_pred):
    predict = K.argmax(y_pred, axis=2)
    y_t = K.argmax(y_true, axis=2)
    num_1_true = K.sum(y_t, axis=1)

    yy = layers.multiply([ predict, y_t ])
    num_1_yy = K.sum(yy, axis=1)
    acc = num_1_yy / num_1_true
    # print(type(acc))
    return acc


def OutWinAcc(y_true, y_pred):
    predict = K.argmax(y_pred, axis=2)
    y_t = K.argmax(y_true, axis=2)
    num_1_true = K.sum(y_t, axis=1)
    num_1_predict = K.sum(predict, axis=1)

    yy = layers.multiply([ predict, y_t ])
    num_1_yy = K.sum(yy, axis=1)
    num_1_outWin = num_1_predict - num_1_yy
    acc = num_1_outWin / num_1_true
    return acc


def Seq2SeqModel():
    X_train, y_train, X_test, y_test, X_validation, y_validation = divideDataByIns(
        '/Users/alafateabulimiti/PycharmProjects/PRD/database/base.txt', 100)

    model = AttentionSeq2Seq(output_dim=output_dim, hidden_dim=hidden_dim, output_length=output_length,
                             input_shape=(input_length, input_dim), depth=3)

    model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=[ 'accuracy', WinAcc, OutWinAcc ])

    YY = [ ]
    for y in y_train:
        YY.append(to_categorical(y))
    YY = np.asarray(YY)
    YYv = [ ]
    #print(YY[ 0 ])
    yyyy = K.argmax(YY, axis=2)
    # print(YY.shape)
    # print(K.get_value(yyyy))
    # print(yyyy.shape)
    for yv in y_validation:
        YYv.append(to_categorical(yv))
    YYv = np.asarray(YYv)
    YYt = [ ]
    for yt in y_test:
        YYt.append(to_categorical(yt))
    YYt = np.asarray(YYt)

    # checkpoint
    filepath = "best_weights.h5"

    checkpoint = ModelCheckpoint(filepath, monitor='acc', verbose=0, mode='auto', period=10)
    callbacks_list = [ checkpoint ]

    history = model.fit(X_train, YY, validation_data=(X_validation, YYv), epochs=100, batch_size=64)
    predict_test = model.predict(X_test)
    # print(predict_test)
    predict = K.argmax(predict_test, axis=2)
    # print(K.get_value(predict).shape)
    # print(K.get_value(predict)[ 10 ])
    # print("------")
    # print(y_test.shape)

    # list all data in history
    print(history.history.keys())
    # summarize history for accuracy
    plt.plot(history.history[ 'acc' ])
    plt.plot(history.history[ 'val_acc' ])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend([ 'train', 'test' ], loc='upper left')
    plt.show()
    # summarize history for loss
    plt.plot(history.history[ 'loss' ])
    plt.plot(history.history[ 'val_loss' ])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend([ 'train', 'test' ], loc='upper left')
    plt.show()


if __name__ == '__main__':
    Seq2SeqModel()
    # val = np.array([ [ 0, 1 ], [ 0, 1 ], [ 0, 1 ], [ 1, 0 ] ,[ 0, 1 ], [ 0, 1 ], [ 0, 1 ], [ 1, 0 ]]).reshape((2,4,2))
    # kvar = K.variable(value=val, dtype='float64', name='example_var')
    # val2 = np.array([ [ 0, 1 ], [ 1, 0 ], [ 0, 1 ], [ 0, 1 ] ,[ 0, 1 ], [ 1, 0 ], [ 1, 0 ], [ 1, 0 ]]).reshape((2,4,2))
    # kvar1 = K.variable(value=val2, dtype='float64', name='example_var2')
    # acc = OutWinAcc(kvar,kvar1)
    # print(K.get_value(acc))
    # yy = layers.multiply([ kvar, kvar1 ])
    # print(K.get_value(kvar / kvar1))
    # print(K.get_value(yy))
    # T = [ ]
    # for v in val:
    #     T.append(to_categorical(v))
    # Tt = np.array(T)
    # print(Tt)
