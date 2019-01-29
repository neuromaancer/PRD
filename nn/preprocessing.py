import numpy as np
import csv
import pandas as pd


def convertRHtoSeq(r, h, size):
    seq = [ str(0) ] * size
    for i in range(len(seq)):
        if not i < r and i < r + h:
            seq[ i ] = str(1)
    seq = ''.join(seq)
    return seq


def preprcessingData(txtfile, size):
    with open(txtfile) as f:
        data = f.readlines()
        data = data[ 2: ]
        num_ins = 1
        with open("database.csv", "a+") as file:
            file.write(str(num_ins) + '\n')
            for line in data:
                if line.count('\n') == len(line):
                    num_ins = num_ins + 1
                    file.write(str(num_ins) + '\n')
                else:
                    l = line.split(' ')
                    r = int(l[ 1 ])
                    h = int(l[ 2 ])
                    seq = convertRHtoSeq(r, h, size)
                    ptime_seq = l[ 5:(size + 5) ]
                    str1 = ' '.join(ptime_seq)
                    file.write("\"" + str(str1) + "\"" + ',' + "\"" + seq + "\"" + "\n")
    return num_ins


def MergeCSV(filelist):
    database = pd.DataFrame([ ])
    for i in range(len(filelist)):
        a = pd.read_csv(filelist[ i ])
        database = database.append(a)
    return database


def divideData(txtfile, size):
    num_instance = preprcessingData(txtfile, size)
    num_ins_test = int(num_instance * 0.2)
    num_ins_validation = num_instance
    num_ins_train = num_instance - num_ins_test * 2
    X_train = [ ]
    y_train = [ ]
    X_test = [ ]
    y_test = [ ]
    X_validation = [ ]
    y_validation = [ ]
    with open('database.csv') as data:
        reader = csv.reader(data)
        dataSet = list(reader)
        # print(dataSet)
        length = len(dataSet)
        count = 0
        for line in dataSet:
            if len(line) == 1:
                count = count + 1
                continue
            if count <= num_ins_train:
                ptimes_list, solved_list = saveLine(line)
                X_train.append(ptimes_list)
                y_train.append(solved_list)
            if num_ins_train < count <= num_ins_train + num_ins_test:
                ptimes_list, solved_list = saveLine(line)
                X_test.append(ptimes_list)
                y_test.append(solved_list)
            if num_ins_train + num_ins_test < count <= num_instance:
                ptimes_list, solved_list = saveLine(line)
                X_validation.append(ptimes_list)
                y_validation.append(solved_list)

    return X_train, y_train, X_test, y_test, X_validation, y_validation


def saveLine(line):
    ptimes = line[ 0 ].split(' ')
    ptimes_list = [ ]
    solved_list = [ ]
    for k in range(0, len(ptimes), 2):
        ptimes_list.append([ int(ptimes[ k ]), int(ptimes[ k + 1 ]) ])
        solved_list.append(list(map(int, line[ 1 ])))
        np.asarray(ptimes_list)
        np.asarray(solved_list)

    return ptimes_list, solved_list


if __name__ == '__main__':
    #num_ins_train = int(59 * 0.6)
    # print(num_ins_train)
    # preprcessingData('Database.txt', 100)
    # print(len(convertRHtoSeq(1, 10, 100)))
    # from random import sample
    #
    #
    # List = [0, 1, 2, 3, 4, 5]
    # print(sample(List, 2))
    # print(sample(List, 2))
    # print(sample(List, 2))
    # print(sample(List, 2))
    # with open('database.csv') as data:
    #     reader = csv.reader(data)
    #     for item in reader:
    #
    #         print(item[0])
    # X_train, y_train, X_test, y_test, X_validation, y_validation = divideData('Database.txt', 100)
    # print(len(X_train)+len(X_test)+len(X_validation))
    # print(y_train)
    # print(X_test)
    # print(y_test)
    # print(X_validation)
    # print(y_validation)
    input_length = 5
    input_dim = 3

    output_length = 3
    output_dim = 4

    samples = 100
    hidden_dim = 24
    x = np.random.random((samples, input_length, input_dim))
    y = np.random.random((samples, output_length, output_dim))
    print(x)
    print('---------------------')
    print(y)