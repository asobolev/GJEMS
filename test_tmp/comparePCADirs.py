import json
import os
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


def getJSONDict(dirPath):
    with open(os.path.join(dirPath, 'morphometrics.json')) as fle:
        return json.load(fle)


def getPCADirs(dirPath, exceptions=None):

    nrns = [x for x in os.listdir(dirPath) if x.endswith('.swc')]

    if exceptions is not None:
        for excep in exceptions:
            nrns.remove(excep)

    pcaDirs = []

    for nrn in nrns:

        jsonDict = getJSONDict(os.path.join(dirPath, nrn.rstrip('.swc') + '_morphData'))

        pcaDirs.append(np.asarray(jsonDict['vectorMeasurements']['pcaDirs']))

    return nrns, pcaDirs


foragerSWCPath = '/home/ajay/PowerFolders/GinJangNDB_Upload/SigenSegmentations/Results/GoodSamplesDLInt1/forager'
newlyEmergedSWCPath = os.path.join('/home/ajay/PowerFolders/GinJangNDB_Upload/SigenSegmentations/Results',
                                   'GoodSamplesDLInt1', 'newlyEmerged')


def plotPCADirs(ax, points, colour, scale=1):

    assert len(points) == 3
    markers = ['s', 'o', '^']
    for pointInd, point in enumerate(points):
        ax.plot([0, scale * point[0]], [0, scale * point[1]], [0, scale * point[2]],
                color=colour, marker=markers[pointInd])
    plt.draw()


fig = plt.figure()
plt.show(block=False)
ax = fig.add_subplot(111, projection='3d')
# foragerNrns, foragerPCADirs = getPCADirs(foragerSWCPath, ['HB130408-1NS.swc'])
foragerNrns, foragerPCADirs = getPCADirs(foragerSWCPath)
for nrnPCADirs in foragerPCADirs:
    plotPCADirs(ax, nrnPCADirs, 'b')
print 'Forager Neurons:', foragerNrns
newlyEmergedNrns, newlyEmergedPCADirs = getPCADirs(newlyEmergedSWCPath)
for nrnPCADirs in newlyEmergedPCADirs:
    plotPCADirs(ax, nrnPCADirs, 'r')
print 'Newly Emerged Neurons:', newlyEmergedNrns