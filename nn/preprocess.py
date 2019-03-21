import numpy as np
import csv


class Preprocess:

    def convertRHtoSeq(self, r, h, size):
        """
        Function can use the numbers : r and h. and create a sequence like (0000011111).
        0: the poisiton out of window
        1: the position in the window
        :param r: start position
        :param h: size of the windows
        :param size: size of the sequence
        :return: the binaire sequence which can give the position of the window(like 00000111000).

        """

        seq = [str(0)] * size
        for i in range(len(seq)):
            if not i < r and i < r + h:
                seq[i] = str(1)
        seq = ''.join(seq)
        return seq

    def preprcessingData(self, txtfile, size):
        """

        Function can extracte the data from the txt generated form the CPLEX program and
        transform to the data form that can be used by the Seq2Seq model.

        :param txtfile: the path of the database txt file.
        :param size: size of the sequence
        :return: the number of the instances and the file csv for the seq2seq

        """

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

                        seq = self.convertRHtoSeq(r, h, size)
                        ptime_seq = l[5:(size * 2 + 5)]
                        # if num_ins < 3:
                        #     print(ptime_seq)
                        #     print(len(ptime_seq))
                        ptimes = ' '.join(ptime_seq)
                        file.write("\"" + str(ptimes) + "\"" + ',' + "\"" + seq + "\"" + "\n")
        return num_ins

    def preprcessingDatawithC(self, txtfile, size):
        """
        Function can extracte the data from the txt generated form the CPLEX program,
        calculate the completion time for each job and add to the database, and
        transform to the data form that can be used by the Seq2Seq model.
        :param txtfile: the path of the database txt file.
        :param size: size of the sequence
        :return: the number of the instances and the file csv for the seq2seq

        """
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

                        seq = self.convertRHtoSeq(r, h, size)
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

    def MergeTXT(self, filenames):
        """
        Function can merge different txt file into one txt file.

        :param filenames: the list of diffrent txt file generated by the CPLEX program.
        :return:
        """

        with open('/Users/alafateabulimiti/PycharmProjects/PRD/database/base.txt', 'w') as outfile:
            for fname in filenames:
                with open(fname) as infile:
                    for line in infile:
                        outfile.write(line)

    def divideData(self, txtfile, size):
        """
        Function can divide the data into 3 part: Training set, Test set and Validation set.

        :param txtfile: the path of the database txt file.
        :param size: size of the sequence
        :return: X_train, y_train, X_test, y_test, X_validation, y_validation
        X_train: Training set which have the initial sequence with processing time.
        y_train: Training set which have the binary sequnece that can indicate the window.
        X_test: Test set which have the initial sequence with processing time.
        y_test: Test set which have the binary sequnece that can indicate the window.
        X_validation: Validation set which have the initial sequence with processing time.
        y_validation: Validation set which have the binary sequnece that can indicate the window.
        """

        num_instance = self.preprcessingData(txtfile, size)
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
                    ptimes_list, solved_list = self.saveLine(line)
                    X_train.append(ptimes_list)
                    y_train.append(solved_list)
                if num_ins_train < count <= num_ins_train + num_ins_test:
                    ptimes_list, solved_list = self.saveLine(line)
                    X_test.append(ptimes_list)
                    y_test.append(solved_list)
                if num_ins_train + num_ins_test < count <= num_instance:
                    ptimes_list, solved_list = self.saveLine(line)
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

    def divideDatawithC(self, txtfile, size):
        """
        Function can divide the data into 3 part: Training set, Test set and Validation set.

        :param txtfile: the path of the database txt file.
        :param size: size of the sequence
        :return: X_train, y_train, X_test, y_test, X_validation, y_validation
        X_train: Training set which have the initial sequence with processing time and completion time.
        y_train: Training set which have the binary sequnece that can indicate the window.
        X_test: Test set which have the initial sequence with processing time and completion time.
        y_test: Test set which have the binary sequnece that can indicate the window.
        X_validation: Validation set which have the initial sequence with processing time and completion time.
        y_validation: Validation set which have the binary sequnece that can indicate the window.

        """

        num_instance = self.preprcessingDatawithC(txtfile, size)
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
                    ptimes_list, solved_list = self.saveLinewithC(line)
                    X_train.append(ptimes_list)
                    y_train.append(solved_list)
                if num_ins_train < count <= num_ins_train + num_ins_test:
                    ptimes_list, solved_list = self.saveLinewithC(line)
                    X_test.append(ptimes_list)
                    y_test.append(solved_list)
                if num_ins_train + num_ins_test < count <= num_instance:
                    ptimes_list, solved_list = self.saveLinewithC(line)
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


    def divideDataByIns(self, txtfile, size):
        """
        Function can divide the data into 3 part: Training set, Test set and Validation set.
        But select only one line of data by instance.

        :param txtfile: the path of the database txt file.
        :param size: size of the sequence
        :return:X_train, y_train, X_test, y_test, X_validation, y_validation
            X_train: Training set which have the initial sequence with processing time.
            y_train: Training set which have the binary sequnece that can indicate the window.
            X_test: Test set which have the initial sequence with processing time.
            y_test: Test set which have the binary sequnece that can indicate the window.
            X_validation: Validation set which have the initial sequence with processing time.
            y_validation: Validation set which have the binary sequnece that can indicate the window.
        """

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
                        ptimes_list, solved_list = self.saveLine(dataSet[i + 1])

                        X_train.append(ptimes_list)
                        y_train.append(solved_list)

                    if num_ins_train < count <= num_ins_train + num_ins_test:
                        ptimes_list, solved_list = self.saveLine(dataSet[i + 1])
                        X_test.append(ptimes_list)
                        y_test.append(solved_list)

                    if num_ins_train + num_ins_test < count <= num_instance:
                        ptimes_list, solved_list = self.saveLine(dataSet[i + 1])
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


    def divideDataByInswithC(self, txtfile, size, num_instance):
        """
        Function can divide the data into 3 part: Training set, Test set and Validation set.
        But select only one line of data by instance.

        :param txtfile: the path of the database txt file.
        :param size: size of the sequence
        :return:X_train, y_train, X_test, y_test, X_validation, y_validation
            X_train: Training set which have the initial sequence with processing time and completion time.
            y_train: Training set which have the binary sequnece that can indicate the window.
            X_test: Test set which have the initial sequence with processing time and completion time.
            y_test: Test set which have the binary sequnece that can indicate the window.
            X_validation: Validation set which have the initial sequence with processing time and completion time.
            y_validation: Validation set which have the binary sequnece that can indicate the window.
        """

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
            for i in range(length):
                if len(dataSet[i]) == 1:
                    count = count + 1
                    if count <= num_ins_train:
                        ptimes_list, solved_list = self.saveLinewithC(dataSet[i + 1])

                        X_train.append(ptimes_list)
                        y_train.append(solved_list)

                    if num_ins_train < count <= num_ins_train + num_ins_test:
                        ptimes_list, solved_list = self.saveLinewithC(dataSet[i + 1])
                        X_test.append(ptimes_list)
                        y_test.append(solved_list)

                    if num_ins_train + num_ins_test < count <= num_instance:
                        ptimes_list, solved_list = self.saveLinewithC(dataSet[i + 1])
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


    def saveLine(self, line):
        """
        Supplement function for bulid the diffrent sets of the seq2seq model

        :param line: one line of the csv file
        :return: ptimes_list, solved_list.
        ptimes_list: the sequence with processing time.
        solved_list: the binary sequence that can indicate the window.
        """

        ptimes = line[0].split(' ')
        ptimes_list = []

        for k in range(0, len(ptimes), 2):
            ptimes_list.append([int(ptimes[k]), int(ptimes[k + 1])])

        solved_list = list(map(int, line[1]))

        np.array(ptimes_list)
        np.array(solved_list)

        return ptimes_list, solved_list


    def saveLinewithC(self, line):
        """
        Supplement function for bulid the diffrent sets of the seq2seq model.

        :param line: one line of the csv file
        :return: ptimes_list, solved_list.

        ptimes_list: the sequence with processing time and completion time.
        solved_list: the binary sequence that can indicate the window.
        """
        ptimes = line[0].split(' ')
        ptimes_list = []
        # print(ptimes)
        for k in range(1, len(ptimes), 4):
            ptimes_list.append(
                [int(float(ptimes[k])), int(float(ptimes[k + 1])), int(float(ptimes[k + 2])),
                 int(float(ptimes[k + 3]))])

        solved_list = list(map(int, line[1]))

        return ptimes_list, solved_list

# num_ins_train = int(59 * 0.6)
# print(num_ins_train)
# preprcessingData('/Users/alafateabulimiti/PycharmProjects/PRD/database/base.txt', 100)

# preprcessingDatawithC('/Users/alafateabulimiti/PycharmProjects/PRD/database/base.txt', 100)
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
