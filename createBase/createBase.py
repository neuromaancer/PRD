import numpy as np
import os, sys
import shutil
import time
from flowshop import compareSeq


def exeTime(func):
    def newFunc(*args, **args2):
        t0 = time.time()
        print("@%s, {%s} start" % (time.strftime("%X", time.localtime()), func.__name__))
        back = func(*args, **args2)
        print("@%s, {%s} end" % (time.strftime("%X", time.localtime()), func.__name__))
        print("@%.3fs taken for {%s}" % (time.time() - t0, func.__name__))
        return back

    return newFunc


def createOptSeq(filePath, seed, tlim):
    os.system("/Users/alafateabulimiti/PycharmProjects/PRD/createBase/F2sumCj.sh" + " " + filePath + " " + str(
        seed) + " " + str(tlim))


@exeTime
def createRbsFile(seqFile, numIt):
    newFile = 'It_' + str(numIt) + '_' + seqFile[:-3] + "rbs"
    shutil.copy(seqFile, newFile)
    r = open(newFile)
    lines = r.readlines()
    r.close()
    w = open(newFile, 'w')
    w.writelines([item for item in lines[:-1]])
    w.close()

    return newFile


def findOrigin(rbsFileWithIter):
    orginInstance = rbsFileWithIter[5:][:-4]
    print(orginInstance)
    return orginInstance


def createtxtFile(rbsFileWithIter):
    seq = np.loadtxt(rbsFileWithIter, dtype=int)[1:]
    print(seq)

    orgintxt = findOrigin(rbsFileWithIter)
    orgintxtArr = np.loadtxt(orgintxt, dtype=int)
    numJobs = len(orgintxtArr)
    numMachine = len(orgintxtArr[0])

    ptimes = np.zeros((numJobs, numMachine))
    for i in range(len(ptimes)):
        ptimes[i] = orgintxtArr[seq[i]]
    ids = np.arange(1, numJobs + 1, 1, dtype=np.int64).reshape(numJobs, 1)
    instance = np.append(ids, ptimes, axis=1)
    instance = np.delete(instance, 1, axis=1)
    np.savetxt(rbsFileWithIter[:-4], instance, fmt='%d %d %d', delimiter=' ')


def calculateI(baseSeqFile, targetSeqFile):
    _, _, baseFO, targetFO = compareSeq(baseSeqFile, targetSeqFile)
    improvement = 1 - (targetFO / baseFO)
    return improvement


def generateBase(exTime, numIt, instancePath):
    begin = time.clock()
    end = 0
    num = 0
    while end < exTime and num < numIt:
        files = os.listdir(instancePath)
        for file in files:
            if file.endswith(".txt"):
                createOptSeq(instancePath + "/" + file, 3, 100)
                createRbsFile(file+".seq",)

        current = time.clock()
        end = current - begin
        num = num + 1


if __name__ == "__main__":
    # generateBase(1000, 1, '/Users/alafateabulimiti/PycharmProjects/PRD/createBase')
    # createOptSeq("/Users/alafateabulimiti/PycharmProjects/PRD/createBase/data.txt",3,10)
    createtxtFile("It_2_data.txt.rbs")
