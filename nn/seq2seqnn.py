from seq2seq.models import AttentionSeq2Seq
import numpy as np
import csv
from nn import preprocess
from sklearn import preprocessing
import os

np.random.seed(1)

from keras.callbacks import LearningRateScheduler
from keras.utils.np_utils import to_categorical
import keras.backend as K
import matplotlib.pyplot as plt
from keras import layers
from keras.callbacks import ModelCheckpoint
from keras import optimizers

input_length = 100
input_dim = 2

output_length = 100
output_dim = 2

samples = 100
hidden_dim = 1000


def WinAcc(y_true, y_pred):
    predict = K.argmax(y_pred, axis=2)
    y_t = K.argmax(y_true, axis=2)
    num_1_true = K.sum(y_t, axis=1)

    yy = layers.multiply([predict, y_t])
    num_1_yy = K.sum(yy, axis=1)
    acc = num_1_yy / num_1_true
    # print(type(acc))
    return acc


def OutWinAcc(y_true, y_pred):
    predict = K.argmax(y_pred, axis=2)
    y_t = K.argmax(y_true, axis=2)
    num_1_true = K.sum(y_t, axis=1)
    num_1_predict = K.sum(predict, axis=1)

    yy = layers.multiply([predict, y_t])
    num_1_yy = K.sum(yy, axis=1)
    num_1_outWin = num_1_predict - num_1_yy
    acc = num_1_outWin / num_1_true
    return acc


def customcrossentropy(y_true, y_pred, weight=0.5):
    predict = K.argmax(y_pred, axis=2)
    predict = K.cast(predict, 'float32')
    # print(K.categorical_crossentropy(y_true, y_pred).shape)
    return layers.multiply([predict, K.categorical_crossentropy(y_true, y_pred)]) * weight + K.categorical_crossentropy(
        y_true,
        y_pred)


def Seq2SeqModel():
    X_train, y_train, X_test, y_test, X_validation, y_validation = preprocess.divideDatawithC(
        '/Users/alafateabulimiti/PycharmProjects/PRD/database/base.txt', 100)

    # test with one instance
    # X_train = []
    # y_train = []
    # with open('databaseC.csv') as data:
    #     reader = csv.reader(data)
    #     dataSet = list(reader)
    #     dataSet = dataSet[1:3]
    #     for line in dataSet:
    #         ptimes_list, solved_list = preprocess.saveLinewithC(line)
    #         # ptimes_list = preprocessing.scale(ptimes_list)
    #         X_train.append(ptimes_list)
    #         y_train.append(solved_list)
    #     X_train = np.asarray(X_train)
    #     y_train = np.asarray(y_train)
    #     y_train = np.reshape(y_train, (len(y_train), 100, 1))

    #     print(X_train[0])
    #     print(y_train[0])

    # X_train = np.random.random((samples, input_length, input_dim))
    # y_train = np.random.random((samples, output_length, 3))
    # y_train = np.reshape(y_train, (len(y_train), 100, 1))
    # y_train = np.argmax(y_train, axis=2)
    # print(X_train[1])
    # print(y_train[1])

    model = AttentionSeq2Seq(output_dim=output_dim, hidden_dim=hidden_dim, output_length=output_length,
                             input_shape=(input_length, 4), depth=3)

    # print(model.summary())
    # model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy', WinAcc, OutWinAcc])
    # model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy', WinAcc, OutWinAcc])
    # model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy', WinAcc, OutWinAcc])
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=[WinAcc, OutWinAcc])

    YY = []
    for y in y_train:
        YY.append(to_categorical(y))
    YY = np.asarray(YY)
    YYv = []
    # print(YY)
    yyyy = K.argmax(YY, axis=2)
    # print(YY.shape)
    # print(K.get_value(yyyy))
    # print(yyyy[1])
    for yv in y_validation:
        YYv.append(to_categorical(yv))
    YYv = np.asarray(YYv)
    YYt = []
    for yt in y_test:
        YYt.append(to_categorical(yt))
    YYt = np.asarray(YYt)

    # checkpoint
    filepath = "best_weights.h5"

    checkpoint = ModelCheckpoint(filepath, monitor='val_WinAcc', save_best_only=True, verbose=0, mode='auto')
    callbacks_list = [checkpoint]

    # history = model.fit(X_train, YY, validation_data=(X_validation, YYv), epochs=2, batch_size=64,
    #                     callbacks=callbacks_list)
    maxfeatures = np.max(np.max(X_train, axis=1), axis=0)
    meanfeatures = np.mean(np.mean(X_train, axis=1), axis=0)
    stdfeatures = np.mean(np.std(X_train, axis=1), axis=0)
    # print(maxfeatures.shape)
    # print(maxfeatures)
    # print(meanfeatures)
    # print(stdfeatures)
    maxfeatures = 1 / maxfeatures
    # X_train=np.multiply(maxfeatures,X_train)
    # X_train=(X_train-meanfeatures)/stdfeatures
    maxfeatures = np.max(np.max(X_train, axis=1), axis=0)
    # print(maxfeatures)
    # input()
    history = model.fit(X_train, YY, epochs=50000, validation_data=(X_validation, YYv), batch_size=64,
                        callbacks=callbacks_list)

    # predict_test = model.predict(X_test)
    # print(predict_test)
    # predict = K.argmax(predict_test, axis=2)
    # print(K.get_value(predict).shape)
    # print(predict_test[10])
    # print("------")
    # print(y_test.shape)

    # list all data in history
    print(history.history.keys())
    # summarize history for accuracy
    # plt.plot(history.history['acc'])

    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

    plt.plot(history.history['WinAcc'])
    plt.plot(history.history['val_WinAcc'])
    plt.title('model WinAcc')
    plt.ylabel('WinAcc')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

    plt.plot(history.history['OutWinAcc'])
    plt.plot(history.history['val_OutWinAcc'])
    plt.title('model OutWinAcc')
    plt.ylabel('OutWinAcc')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()


if __name__ == '__main__':
    os.environ['MKL_NUM_THREADS'] = '3'
    os.environ['GOTO_NUM_THREADS'] = '3'
    os.environ['OMP_NUM_THREADS'] = '3'
    os.environ['openmp'] = 'True'
    # X = []
    # y = []
    # with open('database.csv') as data:
    #     reader = csv.reader(data)
    #     dataSet = list(reader)
    #     dataSet = dataSet[1:7]
    #     for line in dataSet:
    #         ptimes_list, solved_list = preprocessing.saveLine(line)
    #         X.append(ptimes_list)
    #         y.append(solved_list)
    #     X = np.asarray(X)
    #     y = np.asarray(y)
    #     y = np.reshape(y, (len(y), 100, 1))

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
