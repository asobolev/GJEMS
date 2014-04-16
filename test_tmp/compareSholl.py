import json
import os
import numpy as np
import matplotlib.pyplot as plt


def getJSONDict(dirPath):
    with open(os.path.join(dirPath, 'morphometrics.json')) as fle:
        return json.load(fle)


def getShollData(dirPath, exceptions=None):

    nrns = [x for x in os.listdir(dirPath) if x.endswith('.swc')]

    if exceptions is not None:
        for excep in exceptions:
            nrns.remove(excep)

    shollBinData = []
    shollCountData = []


    for nrnInd, nrn in enumerate(nrns):

        jsonDict = getJSONDict(os.path.join(dirPath, nrn.rstrip('.swc') + '_morphData'))

        shollBinData.append(np.asarray(jsonDict['vectorMeasurements']['shollBins']))
        shollCountData.append(np.asarray(jsonDict['vectorMeasurements']['shollCounts']))

    return nrns, shollBinData, shollCountData


def addShollPlot(fig, shollBin, shollCount, colour):

    plt.figure(fig.number)
    plt.plot(shollBin, shollCount, colour + '-o', ms=5, mfc=colour)
    plt.draw()


def drawSholl(fig, shollBins, shollCounts, colour):

    for bins, counts in zip(shollBins, shollCounts):
        addShollPlot(fig, bins, counts, colour)

fig = plt.figure()
plt.show(block=False)

foragerSWCPath = '/home/ajay/PowerFolders/GinJangNDB_Upload/SigenSegmentations/Results/GoodSamplesDLInt1/forager'
newlyEmergedSWCPath = os.path.join('/home/ajay/PowerFolders/GinJangNDB_Upload/SigenSegmentations/Results',
                                   'GoodSamplesDLInt1', 'newlyEmerged')

# foragerNrns, foragerShollBins, foragerShollCounts = getShollData(foragerSWCPath, ['HB130408-1NS.swc'])
foragerNrns, foragerShollBins, foragerShollCounts = getShollData(foragerSWCPath)
NENrns, NEShollBins, NEShollCounts = getShollData(newlyEmergedSWCPath)

drawSholl(fig, foragerShollBins, foragerShollCounts, 'b')
drawSholl(fig, NEShollBins, NEShollCounts, 'r')