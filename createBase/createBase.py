import numpy as np
import os, sys
import shutil
from createBase.compareSeq import compareSeq


def createOptSeq(filePath):
    seed = 3  # random seed for the matheristic program
    tlim = 10000  # limited time for the matheristic program
    os.system("createRbsInstance.sh" + " " + filePath + " " + str(seed) + " " + str(tlim))


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


createRbsFile('data.txt.seq', 2)


def calculateI(baseSeqFile, targetSeqFile):
    _, _, baseFO, targetFO = compareSeq(baseSeqFile, targetSeqFile)
    imporvement = 1 - (targetFO / baseFO)
    return imporvement