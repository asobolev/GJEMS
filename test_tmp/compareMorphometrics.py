import json
import os
import numpy as np
import matplotlib.pyplot as plt


def getJSONDict(dirPath):
    with open(os.path.join(dirPath, 'morphometrics.json')) as fle:
        return json.load(fle)


def getScalarData(dirPath, exceptions=None):
    """
    Takes a directory path with swc Files and _morphData folders and collects all their scalar valued morphomentric data.
    Data will be returned in a 10x<#Nrns> numpy array with the the rows being labeled as (Width, Height, Depth, Length, Volume,
    Surface, NBifs, StdAlongEVec1, StdAlongEVec1, StdAlongEVec1)

    :param dirPath: directory path where the swc files and the corresponding _morphData folders are present.
    :return: numpy array as defined above.
    """

    nrns = [x for x in os.listdir(dirPath) if x.endswith('.swc')]

    if exceptions is not None:
        for excep in exceptions:
            nrns.remove(excep)

    nrnData = np.zeros([10, len(nrns)])

    for nrnInd, nrn in enumerate(nrns):

        jsonDict = getJSONDict(os.path.join(dirPath, nrn.rstrip('.swc') + '_morphData'))

        nrnData[:7, nrnInd] = [jsonDict['scalarMeasurements']['width'],
                              jsonDict['scalarMeasurements']['height'],
                              jsonDict['scalarMeasurements']['depth'],
                              jsonDict['scalarMeasurements']['length'],
                              jsonDict['scalarMeasurements']['volume'],
                              jsonDict['scalarMeasurements']['surface'],
                              jsonDict['scalarMeasurements']['nbifs']]

        nrnData[7:, nrnInd] = jsonDict['vectorMeasurements']['pcaStds']

    return nrnData


def plotDataMatrix(fig, dataMatrix, abcissaValue, yLabels, xlims):

    dataShape = np.shape(dataMatrix)
    nMetrics = dataShape[0]

    assert nMetrics == len(yLabels)

    plt.figure(fig.number)

    nCols = np.ceil(nMetrics / 2.0)
    nRows = 2

    for metricInd in range(nMetrics):

        subplotInd = metricInd + 1
        nNrns = dataShape[1]
        plt.subplot(nRows, nCols, subplotInd)

        plt.plot([abcissaValue] * nNrns, dataMatrix[metricInd, :], 'bo', ms=5, mfc='b')
        plt.ylabel(yLabels[metricInd])
        plt.xlim(xlims)
        plt.ticklabel_format(style='sci', scilimits=(-2, 3), axis='y')

    plt.draw()
    return nRows, nCols


def addMetricToPlot(fig, nRows, nCols, subplotInd, data, abcissaValue, colour, xlims):

    assert len(np.shape(data)) == 1

    plt.figure(fig.number)
    plt.subplot(nRows, nCols, subplotInd)
    plt.plot(abcissaValue * np.ones(np.shape(data)), data, colour + 'o', ms=5, mfc=colour)
    plt.xlim(xlims)
    plt.ticklabel_format(style='sci', scilimits=(-2,3), axis='y')
    plt.draw()




foragerSWCPath = '/home/ajay/PowerFolders/GinJangNDB_Upload/SigenSegmentations/Results/GoodSamplesDLInt1/forager'
newlyEmergedSWCPath = os.path.join('/home/ajay/PowerFolders/GinJangNDB_Upload/SigenSegmentations/Results',
                                   'GoodSamplesDLInt1', 'newlyEmerged')

measureLabels = ['Width', 'Height', 'Depth', 'Total Length', 'Total Volume',
                 'Total Surface', 'Total # of Bifurcations', 'Std along PCA directions']
measureUnits = ['micrometer', 'micrometer', 'micrometer', 'micrometer',
                'cubic micrometer', 'squared micrometer', '#', 'micrometer']


fig = plt.figure()
plt.show(block=False)

# foragerScalarData = getScalarData(foragerSWCPath, ['HB130408-1NS.swc'])

foragerScalarData = getScalarData(foragerSWCPath)

newlyEmergedScalarData = getScalarData(newlyEmergedSWCPath)

nRows, nCols = plotDataMatrix(fig, foragerScalarData[:8, :], 1, [x + '(' + y + ')' for x, y in zip(measureLabels,
                                                                                    measureUnits)], [-0.5, 1.5])

plotDataMatrix(fig, newlyEmergedScalarData[:8, :], 0, [x + '(' + y + ')' for x, y in zip(measureLabels, measureUnits)],
                                                                                                    [-0.5, 1.5])

addMetricToPlot(fig, nRows, nCols, 8, foragerScalarData[8, :], 1, 'r', [-0.5, 1.5])
addMetricToPlot(fig, nRows, nCols, 8, foragerScalarData[9, :], 1, 'g', [-0.5, 1.5])
addMetricToPlot(fig, nRows, nCols, 8, newlyEmergedScalarData[8, :], 0, 'r', [-0.5, 1.5])
addMetricToPlot(fig, nRows, nCols, 8, newlyEmergedScalarData[9, :], 0, 'g', [-0.5, 1.5])

plt.subplot(nRows, nCols, 1)
plt.xlabel('Age')

plt.subplot(nRows, nCols, 8)
plt.title('Each color represents one principle direction')


plt.suptitle('Morphometric Measures v/s Age; Newly Emerged have Age =0, Foragers have Age =1')
