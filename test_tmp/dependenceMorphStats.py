from LMIO.wrapper import *
import numpy as np
import os


swcFilePath = '/home/ajay/PowerFolders/GinJangNDB_Upload/SigenSegmentations/'
neuronIDs = ['HB130408-1']

labor = ['f', 'f', 'f', 'f', 'f', 'ne', 'ne', 'ne']
cols = ['r', 'r', 'r', 'r', 'r', 'b', 'b', 'b']
age = [7, 7, 7, 7, 7, 1, 1, 1]

independentMeasures = ['EucDistance']
dependentMeasures = ['Branch_Order']

measureMeans = np.zeros([len(independentMeasures), len(neuronIDs)])
measureStds = np.zeros([len(independentMeasures), len(neuronIDs)])

for neuronInd, neuronID in enumerate(neuronIDs):

    outputFileName = os.path.join(swcFilePath, neuronID, 'Dependence.npz')

    if not os.path.isfile(outputFileName):
        print 'Saving Dependence of' + str(dependentMeasures) + ' on ' + str(independentMeasures) + ' for ' + neuronID
        neuronSWCDir = os.path.join(swcFilePath, neuronID,'swc')
        dirList = os.listdir(neuronSWCDir)
        nFiles = 2
        swcFiles = [os.path.join(neuronSWCDir, y) for y in dirList[:nFiles] if y.endswith('.swc')]

        nBins = 10
        allHistBins = np.zeros([nFiles, nBins + 1, len(independentMeasures)])
        allBinAverages = np.zeros([nFiles, nBins + 1, len(independentMeasures)])
        allBinStds = np.zeros([nFiles, nBins + 1, len(independentMeasures)])
        output = getMeasureDependence(dependentMeasures, independentMeasures, swcFiles, nBins)
        for measureInd in range(len(independentMeasures)):
            allHistBins[:, :, measureInd] = output[measureInd]['measure1BinCentres']
            allBinAverages[:, :, measureInd] = output[measureInd]['measure2BinAverages']
            allBinStds[:, :, measureInd] = output[measureInd]['measure2BinStdDevs']

        np.savez(outputFileName, allHistBins, allBinAverages, allBinStds)

    else:
        allArrs = np.load(outputFileName)



