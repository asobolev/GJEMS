from LMIO.wrapper import *
import numpy as np
import os
from matplotlib import pyplot as plt

swcFilePath = '/home/ajay/PowerFolders/GinJangNDB_Upload/SigenSegmentations/'
neuronIDs = ['HB130408-1',
              'HB130313-4',
              'HB130322-1',
              'HB130425-1',
              'HB130501-2',
              'HB130605-2',
              'HB130523-3',
              'HB130605-1']

labor = ['f', 'f', 'f', 'f', 'f', 'ne', 'ne', 'ne']
cols = ['r', 'r', 'r', 'r', 'r', 'b', 'b', 'b']
age = [7, 7, 7, 7, 7, 1, 1, 1]
measureNames = ['Width', 'Height', 'Depth', 'Length', 'Volume', 'Surface', 'N_bifs']
measureLabels = ['Width', 'Height', 'Depth', 'Total Length', 'Total Volume', 'Total Surface', 'Total # of Bifurcations']
measureUnits = ['micrometer', 'micrometer', 'micrometer', 'micrometer', 'cubic micrometer', 'squared micrometer','#']

measureMeans = np.zeros([len(measureNames), len(neuronIDs)])
measureStds = np.zeros([len(measureNames), len(neuronIDs)])

for neuronInd, neuronID in enumerate(neuronIDs):

    outputFileName = os.path.join(swcFilePath, neuronID, 'WholeCellPropertiesTest.npy')

    if not os.path.isfile(outputFileName):
        print 'Saving Whole Cell properties for ' + neuronID
        neuronSWCDir = os.path.join(swcFilePath, neuronID,'swc')
        dirList = os.listdir(neuronSWCDir)
        # nFiles = len(dirList)
        nFiles = 1
        swcFiles = [os.path.join(neuronSWCDir, y) for y in dirList[:nFiles] if y.endswith('.swc')]

        allStats = np.zeros([len(measureNames), nFiles])
        output = getMeasure(measureNames, swcFiles)
        for measureInd in range(len(measureNames)):
            allStats[measureInd, :] = output[measureInd]['WholeCellMeasures'][:, 0]

        np.save(outputFileName, allStats)

    else:
        allStats = np.load(outputFileName)

    measureMeans[:, neuronInd] = np.mean(allStats,axis=1)
    measureStds[:, neuronInd] = np.std(allStats,axis=1)

plt.figure()
plt.show(block=False)
for measureInd in xrange(len(measureNames)):
    plt.subplot(2,4,measureInd+2)
    for neuronInd in xrange(len(neuronIDs)):
        lable = '__nolegend__'

        if (measureInd==0) and (neuronInd == 0):
            lable = 'Forager'
        if (measureInd==0) and (neuronInd == 7):
            lable = 'Newly Emerged'

        plt.errorbar([neuronInd], measureMeans[measureInd,neuronInd],measureStds[measureInd, neuronInd],
                     ecolor=cols[neuronInd], marker='o', mfc=cols[neuronInd], ms=5, ls='None', label=lable)
    plt.ylabel(measureLabels[measureInd] + ' (' + measureUnits[measureInd] + ')')
    plt.ticklabel_format(style='sci', scilimits=(-2,3), axis='y',)
    plt.xlim(-1,8)
    plt.xticks([])

plt.subplot(2,4,2)
plt.legend(loc = 'upper left', bbox_to_anchor = (-1.2, 0.5))
plt.draw()
