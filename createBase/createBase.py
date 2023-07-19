import numpy as np
import os,linecache, shutil, time, csv
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
    return f"{filePath}.seq"


def createOptSeqWin(filePath, seed, tlim):
    # os.system(r"C:\Users\Alafat~1\Documents\PRD\Matho\F2SumCj.exe" + ' ' + filePath + " " + str(
    #     seed) + " " + str(tlim))
    os.system(r"C:\Users\21606250t\PycharmProjects\PRD\Matho\F2SumCj.exe" + ' ' + filePath + " " + str(
        seed) + " " + str(tlim))
    return f"{filePath}.seq"


def createRbsFile(seqFile, numIt):
    if seqFile[:2] == "It":
        newFile = f'It_{str(numIt)}_{seqFile[:-3][5:]}rbs'
    else:
        newFile = f'It_{str(numIt)}_{seqFile[:-3]}rbs'

    shutil.copy(seqFile, newFile)
    with open(newFile) as r:
        lines = r.readlines()
    with open(newFile, 'w') as w:
        w.writelines(list(lines[:-1]))
    return newFile


def findOrigin(rbsFileWithIter):
    return rbsFileWithIter[5:][:-4]


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
    return 1 - (targetFO / baseFO)


def extractFOfromFile(file):
    f = open(file)
    rbs = f.readline().split(" ")
    return int(rbs[0])


def extractRH(seqfile):
    rh = linecache.getline(seqfile, 2).split(" ")
    r = rh[0]
    h = rh[1]
    return r, h


def extractSeq(file):
    f = open(file)
    seq = f.readline().split(' ')
    seq = seq[2:-1]
    return seq


def extractSeqWithIns(file, instanceFile):
    seq = extractSeq(file)
    seqWithIns = []
    for i in seq:
        ptime = linecache.getline(instanceFile, int(i) + 1).split(" ")
        seqWithIns.append([int(ptime[1]), int(ptime[2][:-1])])
    return seqWithIns


def generateBaseForOneIns(exTime, numIt, instanceFile):
    begin = time.clock()
    end = 0
    num = 1
    inirbsFile = f"{instanceFile}.rbs"
    initFO = extractFOfromFile(inirbsFile)
    newinstancefile = instanceFile
    while end < exTime and num < numIt:
        seqfile = createOptSeqWin(newinstancefile, 3, 200)
        if os.stat(seqfile).st_size == 0:
            break
        rbsfile = createRbsFile(seqfile, num)
        optFO = extractFOfromFile(seqfile)
        rbsFO = extractFOfromFile(rbsfile)
        I = calculateI(initFO, rbsFO)
        Iprime = calculateI(initFO, optFO)
        r, h = extractRH(seqfile)
        S = extractSeqWithIns(rbsfile, newinstancefile)
        Sprime = extractSeqWithIns(seqfile, newinstancefile)
        with open("base.csv", "a+",newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([S, Sprime, r, h, I, Iprime])
        newinstancefile = createtxtFile(rbsfile)
        current = time.clock()
        end = current - begin
        num += 1

def generationBase(instancePath):
    files = os.listdir(instancePath)
    for file in files:
        if file.endswith(".txt"):
            createOptSeqWin(file,3,10000000)

if __name__ == "__main__":
    # createOptSeq("/Users/alafateabulimiti/PycharmProjects/PRD/createBase/data.txt",3,10)
    # createtxtFile("It_2_data.txt.rbs")
    # createOptSeqWin("It_1_data.txt", 3, 100)
    #generateBaseForOneIns(300, 3, "data.txt")
    # createRbsFile("It_1_data.txt.seq", 2)
    # extractSeq("data.txt.rbs")
    # seq = extractSeqWithIns("It_1_data.txt.rbs", "It_1_data.txt")
    # print(len(seq))
    generationBase(r"C:\Users\21606250t\PycharmProjects\PRD\createBase")