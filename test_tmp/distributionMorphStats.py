from LMIO.wrapper import *
import numpy as np
import os
from matplotlib import pyplot as plt

swcFilePath = '/home/ajay/PowerFolders/GinJangNDB_Upload/SigenSegmentations/'
neuronIDs = ['HB130408-1']

labor = ['f', 'f', 'f', 'f', 'f', 'ne', 'ne', 'ne']
cols = ['r', 'r', 'r', 'r', 'r', 'b', 'b', 'b']
age = [7, 7, 7, 7, 7, 1, 1, 1]

measureNames = ['Diameter']

measureMeans = np.zeros([len(measureNames), len(neuronIDs)])
measureStds = np.zeros([len(measureNames), len(neuronIDs)])

for neuronInd, neuronID in enumerate(neuronIDs):

    outputFileName = os.path.join(swcFilePath, neuronID, measureNames[0] + 'Distribution.npz')

    if not os.path.isfile(outputFileName):
        print 'Saving ' + str(measureNames) + 'Distribution(s) for ' + neuronID
        neuronSWCDir = os.path.join(swcFilePath, neuronID,'swc')
        dirList = os.listdir(neuronSWCDir)
        nFiles = 2
        swcFiles = [os.path.join(neuronSWCDir, y) for y in dirList[:nFiles] if y.endswith('.swc')]

        nBins = 10
        allHistBins = np.zeros([nFiles, nBins + 1, len(measureNames)])
        allHistCounts = np.zeros([nFiles, nBins + 1, len(measureNames)])
        output = getMeasureDistribution(measureNames, swcFiles, nBins)
        for measureInd in range(len(measureNames)):
            allHistBins[:, :, measureInd] = output[measureInd]['measure1BinCentres']
            allHistCounts[:, :, measureInd] = output[measureInd]['measure1BinCounts']

        np.savez(outputFileName, allHistBins, allHistCounts)

    else:
        allArrs = np.load(outputFileName)


