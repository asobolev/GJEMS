import json
import os
import numpy as np
import matplotlib.pyplot as plt


def getJSONDict(dirPath):
    with open(os.path.join(dirPath, 'morphometrics.json')) as fle:
        return json.load(fle)


def getScalarData(nrns):
    """
    Takes a list of swc Files and using _morphData folders to collect their scalar valued morphomentric data.
    Data will be returned in a 10x<#Nrns> numpy array with the the rows being labeled as (Width, Height, Depth, Length, Volume,
    Surface, NBifs, StdAlongEVec1, StdAlongEVec1, StdAlongEVec1)

    :param nrns: list of swc files and the corresponding _morphData folders are present.
    :return: numpy array as defined above.
    """

    nrnData = np.zeros([10, len(nrns)])

    for nrnInd, nrn in enumerate(nrns):

        jsonDict = getJSONDict(nrn.rstrip('.swc') + '_morphData')

        nrnData[:7, nrnInd] = [jsonDict['scalarMeasurements']['width'],
                               jsonDict['scalarMeasurements']['height'],
                               jsonDict['scalarMeasurements']['depth'],
                               jsonDict['scalarMeasurements']['length'],
                               jsonDict['scalarMeasurements']['volume'],
                               jsonDict['scalarMeasurements']['surface'],
                               jsonDict['scalarMeasurements']['nbifs']]

        nrnData[7:, nrnInd] = jsonDict['vectorMeasurements']['pcaStds']

    return nrnData


def plotDataMatrix(fig, dataMatrix, abcissaValue, yLabels, xlims, col, maerker):

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

        plt.plot([abcissaValue] * nNrns, dataMatrix[metricInd, :], color=col, marker=maerker, ms=5, mfc=col)
        plt.ylabel(yLabels[metricInd])
        plt.xlim(xlims)
        plt.ticklabel_format(style='sci', scilimits=(-2, 3), axis='y')

    plt.draw()
    return nRows, nCols


def addMetricToPlot(fig, nRows, nCols, subplotInd, data, abcissaValue, colour, xlims, maerker):

    assert len(np.shape(data)) == 1

    plt.figure(fig.number)
    plt.subplot(nRows, nCols, subplotInd)
    plt.plot(abcissaValue * np.ones(np.shape(data)), data, color=colour, marker=maerker, ms=5, mfc=colour)
    plt.xlim(xlims)
    plt.ticklabel_format(style='sci', scilimits=(-2,3), axis='y')
    plt.draw()


nrnH = '/home/ajay/repos/GJEMS/test_tmp/swcFiles/GoodSamplesDLInt1_v2/HB130408-1NS/012_all_H.swc'
nrnL = '/home/ajay/repos/GJEMS/test_tmp/swcFiles/GoodSamplesDLInt1_v2/HB130408-1NS/012_all_L.swc'
nrnV1 = '/home/ajay/PowerFolders/GinJangNDB_Upload/SigenSegmentations/Results/GoodSamplesDLInt1_v1/forager/' \
            + 'HB130408-1NS_3ptSoma.swc'



measureLabels = ['Width', 'Height', 'Depth', 'Total Length', 'Total Volume',
                 'Total Surface', 'Total # of Bifurcations', 'Std along PCA directions']
measureUnits = ['micrometer', 'micrometer', 'micrometer', 'micrometer',
                'cubic micrometer', 'squared micrometer', '#', 'micrometer']


fig = plt.figure()
plt.show(block=False)

# foragerScalarData = getScalarData(foragerSWCPath, ['HB130408-1NS.swc'])

nrnHData = getScalarData([nrnH])

nrnLData = getScalarData([nrnL])

nrnV1Data = getScalarData([nrnV1])

nRows, nCols = plotDataMatrix(fig, nrnLData[:8, :], 1,
                              [x + '(' + y + ')' for x, y in zip(measureLabels, measureUnits)],
                              [0, 1.5], 'b', 'o')

plotDataMatrix(fig, nrnHData[:8, :], 0.5, [x + '(' + y + ')' for x, y in zip(measureLabels, measureUnits)],
               [0, 1.5], 'b', 'o')

plotDataMatrix(fig, nrnV1Data[:8, :], 1, [x + '(' + y + ')' for x, y in zip(measureLabels, measureUnits)],
               [0, 1.5], 'b', '*')

addMetricToPlot(fig, nRows, nCols, 8, nrnLData[8, :], 1, 'r', [0, 1.5], 'o')
addMetricToPlot(fig, nRows, nCols, 8, nrnLData[9, :], 1, 'g', [0, 1.5], 'o')
addMetricToPlot(fig, nRows, nCols, 8, nrnHData[8, :], 0.5, 'r', [0, 1.5], 'o')
addMetricToPlot(fig, nRows, nCols, 8, nrnHData[9, :], 0.5, 'g', [0, 1.5], 'o')
addMetricToPlot(fig, nRows, nCols, 8, nrnV1Data[8, :], 1, 'r', [0, 1.5], '*')
addMetricToPlot(fig, nRows, nCols, 8, nrnV1Data[9, :], 1, 'g', [0, 1.5], '*')


plt.subplot(nRows, nCols, 1)
plt.xlabel('Resolution of imaging(micrometer)')

plt.subplot(nRows, nCols, 8)
plt.title('Each color represents one principle direction')


plt.suptitle('Morphometric Measures of HB130408-1NS. Circles are for new reconstructions(v2, Apr 2014) '
             + 'and asterisk for old reconstruction(v1, Feb 2014) ')
