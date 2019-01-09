import numpy as np
import os, sys
import shutil
import time
import linecache
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


def createOptSeqOSX(filePath, seed, tlim):
    os.system("/Users/alafateabulimiti/PycharmProjects/PRD/createBase/F2sumCj.sh" + " " + filePath + " " + str(
        seed) + " " + str(tlim))
    return filePath + ".seq"




def createRbsFile(seqFile, numIt):
    if seqFile[0:2] == "It":
        newFile = 'It_' + str(numIt) + '_' + seqFile[:-3][5:] + "rbs"
    else:
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
    return orginInstance


def createtxtFile(rbsFileWithIter):
    seq = np.loadtxt(rbsFileWithIter, dtype=int)[1:]

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
    filename = rbsFileWithIter[:-4]
    np.savetxt(filename, instance, fmt='%d %d %d', delimiter=' ')

    return filename


def calculateI(baseFO, targetFO):
    improvement = 1 - (targetFO / baseFO)
    return improvement


def extractFOfromFile(file):
    f = open(file)
    rbs = f.readline().split(" ")
    initFO = int(rbs[0])
    return initFO


def extractRH(seqfile):
    rh = linecache.getline(seqfile, 2).split(" ")
    r = rh[0]
    h = rh[1]
    return r, h


def generateBaseForOneIns(exTime, numIt, instanceFile):
    begin = time.clock()
    end = 0
    num = 1
    inirbsFile = instanceFile + ".rbs"
    initFO = extractFOfromFile(inirbsFile)
    newinstancefile = instanceFile
    while end < exTime and num < numIt:
        seqfile = createOptSeqOSX(newinstancefile, 3, 200)
        rbsfile = createRbsFile(seqfile, num)
        optFO = extractFOfromFile(seqfile)
        rbsFO = extractFOfromFile(rbsfile)
        I = calculateI(initFO, rbsFO)
        Iprime = calculateI(initFO, optFO)
        r, h = extractRH(seqfile)
        newinstancefile = createtxtFile(rbsfile)
        print(r, h, I, Iprime)
        current = time.clock()
        end = current - begin
        num = num + 1


if __name__ == "__main__":
    # generateBase(1000, 1, '/Users/alafateabulimiti/PycharmProjects/PRD/createBase')
    # createOptSeq("/Users/alafateabulimiti/PycharmProjects/PRD/createBase/data.txt",3,10)
    # createtxtFile("It_2_data.txt.rbs")
    # createOptSeq("data.txt", 3, 100)
    generateBaseForOneIns(300, 3, "data.txt")
    # createRbsFile("It_1_data.txt.seq", 2)
