from LMIO.wrapper import *
import numpy as np
import os
from matplotlib import pyplot as plt
from scipy.stats import pearsonr

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

volNBifsCorr = []

for neuronInd, neuronID in enumerate(neuronIDs):

    outputFileName = os.path.join(swcFilePath, neuronID, 'WholeCellProperties.npy')

    if not os.path.isfile(outputFileName):
        print 'Saving Whole Cell properties for ' + neuronID
        neuronSWCDir = os.path.join(swcFilePath, neuronID,'swc')
        dirList = os.listdir(neuronSWCDir)
        nFiles = len(dirList)
        swcFiles = [os.path.join(neuronSWCDir, y) for y in dirList[:nFiles] if y.endswith('.swc')]

        lmio = LMIO()
        allStats = np.zeros([len(measureNames), nFiles])
        output = lmio.getMeasure(measureNames, swcFiles)
        for measureInd in range(len(measureNames)):
            allStats[measureInd, :] = output[measureInd]['WholeCellMeasures'][:, 0]

        outputFileName = os.path.join(swcFilePath, neuronID, 'WholeCellProperties.npy')
        np.save(outputFileName, allStats)

    else:
        allStats = np.load(outputFileName)

    volNBifsCorr.append(pearsonr(allStats[4,:], allStats[6,:])[0])