import numpy as np


def CreateInstance(numJobs, numMachine):
    ptime = np.random.randint(10, 100, size=[numJobs, numMachine])
    ids = np.arange(1, numJobs + 1, 1, dtype=np.int64).reshape(numJobs, 1)
    instance = np.append(ids, ptime, axis=1)
    np.savetxt('C:/Users/Alafate ABULIMITI/Documents/PRD/instances/data.txt', instance, fmt='%d %d %d',
               delimiter=' ')
    return instance

CreateInstance(20,2)
