import numpy as np
import time

def createInstance(numJobs, numInstance, numMachine =2):
    '''
    create the instances, the processing times are random but between 10 and 100 units of time
    :param numJobs: number of the jobs 
    :param numInstance: number of the instances
    :param numMachine: number of the machines(2 is number by default)
    :return: the txt files create in the intances folder
    '''
    for i in range(numInstance):
        ptime = np.random.randint(10, 100, size=[numJobs, numMachine])
        ids = np.arange(1, numJobs + 1, 1, dtype=np.int64).reshape(numJobs, 1)
        instance = np.append(ids, ptime, axis=1)
        np.savetxt('/Users/alafateabulimiti/PycharmProjects/PRD/instances/' + str(numJobs) + 'jobs_'
                   + str(i) + '_' + time.strftime("%d-%m-%Y", time.localtime()) + '.txt',
                   instance, fmt='%d %d %d', delimiter=' ')

createInstance(100, 20)
