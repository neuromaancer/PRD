import numpy as np

def CreateInstance(numJobs, numMachine):
    instance = np.random.randint(10, 100, size=[numJobs, numMachine])
    np.savetxt('/Users/alafateabulimiti/PycharmProjects/PRD/instances/new.csv', instance,fmt ='%d,%d', delimiter=',')
    return instance

