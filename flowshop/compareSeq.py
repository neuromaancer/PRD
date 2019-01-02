import numpy as np

def compareSeq(baseFileName, targetFileName):
    '''
    compare two sequences files and extract the 'real' r and h
    :param baseFileName: the reference file
    :param targetFileName: the file we want to calulate the r and h
    :return:
        1. r: the start position
        2. h: the scale of the window
        3. baseFO: the value of the objective fonction of the reference file
        4. targetFo: the value of the objective fonction of the target file
    '''
    base = np.loadtxt(baseFileName, dtype=int)
    target = np.loadtxt(targetFileName, dtype=int)
    baseFO = base[0]
    targetFO = target[0]
    base = base[1:]
    target = target[1:]

    for r in range(len(base)):
        if base[r] != target[r]:
            break

    for h in range(len(base)-1, -1, -1):
        if base[h] != target[h]:
            break

    return r, h, baseFO, targetFO

