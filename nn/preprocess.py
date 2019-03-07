import numpy as np
import csv
import pandas as pd


def convertRHtoSeq(r, h, size):
    seq = [str(0)] * size
    for i in range(len(seq)):
        if not i < r and i < r + h:
            seq[i] = str(1)
    seq = ''.join(seq)
    return seq


def preprcessingData(txtfile, size):
    with open(txtfile) as f:
        data = f.readlines()
        data = data[2:]
        num_ins = 1
        with open("database.csv", "a+") as file:
            file.write(str(num_ins) + '\n')
            for line in data:
                if line.count('\n') == len(line):
                    num_ins = num_ins + 1
                    file.write(str(num_ins) + '\n')
                else:
                    l = line.split(' ')
                    r = int(l[1])
                    h = int(l[2])
                    # print(str(r) + '\t' +str(h))

                    seq = convertRHtoSeq(r, h, size)
                    ptime_seq = l[5:(size * 2 + 5)]
                    # if num_ins < 3:
                    #     print(ptime_seq)
                    #     print(len(ptime_seq))
                    ptimes = ' '.join(ptime_seq)
                    file.write("\"" + str(ptimes) + "\"" + ',' + "\"" + seq + "\"" + "\n")
    return num_ins


def preprcessingDatawithC(txtfile, size):
    with open(txtfile) as f:
        data = f.readlines()
        data = data[2:]
        num_ins = 1
        with open("databaseC.csv", "a+") as file:
            file.write(str(num_ins) + '\n')
            for line in data:
                if line.count('\n') == len(line):
                    num_ins = num_ins + 1
                    file.write(str(num_ins) + '\n')
                else:
                    l = line.split(' ')
                    r = int(l[1])
                    h = int(l[2])
                    # print(str(r) + '\t' +str(h))

                    seq = convertRHtoSeq(r, h, size)
                    ptime_seq = l[5:(size * 2 + 5)]
                    # print(ptime_seq)
                    file.write("\"")
                    # ptimes = ' '.join(ptime_seq)
                    C1 = 0
                    C2 = 0
                    for i in range(0, len(ptime_seq), 2):
                        file.write(" " + ptime_seq[i] + " " + ptime_seq[i + 1] + " ")
                        C1 += int(ptime_seq[i])
                        C2 = max(C1 + int(ptime_seq[i + 1]), C2 + int(ptime_seq[i + 1]))
                        file.write(str(C1) + " " + str(C2))
                    file.write("\"")
                    # if num_ins < 3:
                    #     print(ptime_seq)
                    #     print(len(ptime_seq))
                    ptimes = ' '.join(ptime_seq)
                    file.write(',' + "\"" + seq + "\"" + "\n")
    return num_ins


def MergeTXT(filenames):
    with open('/Users/alafateabulimiti/PycharmProjects/PRD/database/base.txt', 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)


def divideData(txtfile, size):
    num_instance = preprcessingData(txtfile, size)
    num_ins_test = int(num_instance * 0.2)
    num_ins_validation = num_ins_test
    num_ins_train = num_instance - num_ins_test * 2
    X_train = []
    y_train = []
    X_test = []
    y_test = []
    X_validation = []
    y_validation = []
    with open('database.csv') as data:
        reader = csv.reader(data)
        dataSet = list(reader)
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
    X_train = np.asarray(X_train)
    y_train = np.asarray(y_train)
    y_train = np.reshape(y_train, (len(y_train), size, 1))
    X_test = np.asarray(X_test)
    y_test = np.asarray(y_test)
    y_test = np.reshape(y_test, (len(y_test), size, 1))
    X_validation = np.asarray(X_validation)
    y_validation = np.asarray(y_validation)
    y_validation = np.reshape(y_validation, (len(y_validation), size, 1))
    return X_train, y_train, X_test, y_test, X_validation, y_validation


def divideDatawithC(txtfile, size):
    num_instance = preprcessingDatawithC(txtfile, size)
    print("num_instance: " + str(num_instance))
    num_ins_test = int(num_instance * 0.2)
    num_ins_validation = num_ins_test
    num_ins_train = num_instance - num_ins_test * 2
    X_train = []
    y_train = []
    X_test = []
    y_test = []
    X_validation = []
    y_validation = []
    with open('databaseC.csv') as data:
        reader = csv.reader(data)
        dataSet = list(reader)
        length = len(dataSet)
        count = 0
        for line in dataSet:
            if len(line) == 1:
                count = count + 1
                continue
            if count <= num_ins_train:
                ptimes_list, solved_list = saveLinewithC(line)
                X_train.append(ptimes_list)
                y_train.append(solved_list)
            if num_ins_train < count <= num_ins_train + num_ins_test:
                ptimes_list, solved_list = saveLinewithC(line)
                X_test.append(ptimes_list)
                y_test.append(solved_list)
            if num_ins_train + num_ins_test < count <= num_instance:
                ptimes_list, solved_list = saveLinewithC(line)
                X_validation.append(ptimes_list)
                y_validation.append(solved_list)
    X_train = np.asarray(X_train)
    y_train = np.asarray(y_train)
    y_train = np.reshape(y_train, (len(y_train), size, 1))
    X_test = np.asarray(X_test)
    y_test = np.asarray(y_test)
    y_test = np.reshape(y_test, (len(y_test), size, 1))
    X_validation = np.asarray(X_validation)
    y_validation = np.asarray(y_validation)
    y_validation = np.reshape(y_validation, (len(y_validation), size, 1))
    return X_train, y_train, X_test, y_test, X_validation, y_validation


def divideDataByIns(txtfile, size):
    num_instance = 1625
    num_ins_test = int(num_instance * 0.2)
    num_ins_validation = num_ins_test
    num_ins_train = num_instance - num_ins_test * 2
    X_train = []
    y_train = []
    X_test = []
    y_test = []
    X_validation = []
    y_validation = []
    with open('database.csv') as data:
        reader = csv.reader(data)
        dataSet = list(reader)
        length = len(dataSet)
        count = 0
        for i in range(length):
            if len(dataSet[i]) == 1:
                count = count + 1
                if count <= num_ins_train:
                    ptimes_list, solved_list = saveLine(dataSet[i + 1])

                    X_train.append(ptimes_list)
                    y_train.append(solved_list)

                if num_ins_train < count <= num_ins_train + num_ins_test:
                    ptimes_list, solved_list = saveLine(dataSet[i + 1])
                    X_test.append(ptimes_list)
                    y_test.append(solved_list)

                if num_ins_train + num_ins_test < count <= num_instance:
                    ptimes_list, solved_list = saveLine(dataSet[i + 1])
                    X_validation.append(ptimes_list)
                    y_validation.append(solved_list)

    X_train = np.asarray(X_train)
    y_train = np.asarray(y_train)
    y_train = np.reshape(y_train, (len(y_train), size, 1))
    X_test = np.asarray(X_test)
    y_test = np.asarray(y_test)
    y_test = np.reshape(y_test, (len(y_test), size, 1))
    X_validation = np.asarray(X_validation)
    y_validation = np.asarray(y_validation)
    y_validation = np.reshape(y_validation, (len(y_validation), size, 1))
    return X_train, y_train, X_test, y_test, X_validation, y_validation


def saveLine(line):
    ptimes = line[0].split(' ')
    ptimes_list = []

    for k in range(0, len(ptimes), 2):
        ptimes_list.append([int(ptimes[k]), int(ptimes[k + 1])])

    solved_list = list(map(int, line[1]))

    np.array(ptimes_list)
    np.array(solved_list)

    return ptimes_list, solved_list


def saveLinewithC(line):
    ptimes = line[0].split(' ')
    ptimes_list = []
    # print(ptimes)
    for k in range(1, len(ptimes), 4):
        ptimes_list.append(
            [int(float(ptimes[k])), int(float(ptimes[k + 1])), int(float(ptimes[k + 2])), int(float(ptimes[k + 3]))])

    solved_list = list(map(int, line[1]))

    np.array(ptimes_list)
    np.array(solved_list)

    return ptimes_list, solved_list


if __name__ == '__main__':
    # num_ins_train = int(59 * 0.6)
    # print(num_ins_train)
    # preprcessingData('/Users/alafateabulimiti/PycharmProjects/PRD/database/base.txt', 100)
    preprcessingDatawithC('/Users/alafateabulimiti/PycharmProjects/PRD/database/base.txt', 100)
    # print(convertRHtoSeq(1, 10, 100))
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
    # X_train, y_train, X_test, y_test, X_validation, y_validation = divideDataByIns('/Users/alafateabulimiti/PycharmProjects/PRD/database/base.txt', 100)
    # print(len(X_train)+len(X_test)+len(X_validation))
    # print(X_train)
    # print(len(y_train))
    # print(X_train.shape)
    # print(y_test)
    # print(X_validation)
    # print(y_validation)
    # input_length = 5
    # input_dim = 3
    #
    # output_length = 3
    # output_dim = 4
    #
    # samples = 100
    # hidden_dim = 24
    # x = np.random.random((samples, input_length, input_dim))
    # y = np.random.random((samples, output_length, output_dim))
    # print(x)
    # print('---------------------')
    # print(y)
    # filenames = ['/Users/alafateabulimiti/PycharmProjects/PRD/database/Database.txt','/Users/alafateabulimiti/PycharmProjects/PRD/database/Database2.txt','/Users/alafateabulimiti/PycharmProjects/PRD/database/Database3.txt']
    # MergeTXT([ '/Users/alafateabulimiti/PycharmProjects/PRD/database/Database1.txt',
    #            '/Users/alafateabulimiti/PycharmProjects/PRD/database/Database2.txt',
    #            '/Users/alafateabulimiti/PycharmProjects/PRD/database/Database3.txt',
    #            '/Users/alafateabulimiti/PycharmProjects/PRD/database/Database4.txt',
    #            '/Users/alafateabulimiti/PycharmProjects/PRD/database/Database5.txt',
    #            '/Users/alafateabulimiti/PycharmProjects/PRD/database/Database6.txt',
    #            '/Users/alafateabulimiti/PycharmProjects/PRD/database/Database7.txt',
    #            '/Users/alafateabulimiti/PycharmProjects/PRD/database/Database8.txt',
    #            '/Users/alafateabulimiti/PycharmProjects/PRD/database/Database9.txt',
    #            '/Users/alafateabulimiti/PycharmProjects/PRD/database/Database10.txt',
    #            '/Users/alafateabulimiti/PycharmProjects/PRD/database/Database11.txt',
    #            '/Users/alafateabulimiti/PycharmProjects/PRD/database/Database12.txt',
    #            '/Users/alafateabulimiti/PycharmProjects/PRD/database/Database13.txt',
    #            '/Users/alafateabulimiti/PycharmProjects/PRD/database/Database14.txt',
    #            '/Users/alafateabulimiti/PycharmProjects/PRD/database/Database15.txt',
    #            '/Users/alafateabulimiti/PycharmProjects/PRD/database/Database16.txt',
    #            '/Users/alafateabulimiti/PycharmProjects/PRD/database/Database17.txt',
    #            '/Users/alafateabulimiti/PycharmProjects/PRD/database/Database18.txt',
    #            '/Users/alafateabulimiti/PycharmProjects/PRD/database/Database19.txt',
    #            '/Users/alafateabulimiti/PycharmProjects/PRD/database/Database20.txt',
    #            '/Users/alafateabulimiti/PycharmProjects/PRD/database/Database21.txt',
    #            '/Users/alafateabulimiti/PycharmProjects/PRD/database/Database22.txt',
    #            '/Users/alafateabulimiti/PycharmProjects/PRD/database/Database23.txt',
    #            ])
