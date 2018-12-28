import numpy as np

def compareSeq(baseFileNme, targetFileName):
    base = np.loadtxt(baseFileNme, dtype=int)
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

print(compareSeq('data.txt.rbs','data.txt.seq'))

