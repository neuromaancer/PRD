import numpy as np
import os
import shutil


def createOptSeq(filePath):
    seed = 3  # random seed for the matheristic program
    tlim = 10000  # limited time for the matheristic program
    os.system("createRbsInstance.sh" + " " + filePath + " " + str(seed) + " " + str(tlim))

def createRbsfile(seqFile, numIt):
    shutil.copy(seqFile, str(numIt) + '_' + seqFile[:-3] + "rbs")

