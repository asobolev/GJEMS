from GJEMS.morph.morph import rotatePts2D, plotPoints3D, addPoints3D
import matplotlib.pyplot as plt
from easygui import fileopenbox
import numpy as np
import os
import subprocess
import json


def getSWCFiles(dirPath, exceptions=None):
    """
    Takes a directory path with swc Files and returns the paths of all swc files in the path except those in exceptions.

    :param dirPath: directory path where the swc files and the corresponding _morphData folders are present.
    :return: list of swc file paths
    """

    nrns = [x for x in os.listdir(dirPath) if x.endswith('.swc')]

    if exceptions is not None:
        print exceptions, nrns
        for excep in exceptions:
            nrns.remove(excep)

    return [os.path.join(dirPath, x) for x in nrns]


def getAZ2D(swcFile):
    output = subprocess.check_output(['python', 'getAZ2D.py', swcFile])
    startStr = 'startJSON'
    return json.loads(output[output.find(startStr) + len(startStr): -1])


plt.figure()
plt.show(block=False)

# foragerSWCPath = '/home/ajay/PowerFolders/GinJangNDB_Upload/SigenSegmentations/Results/GoodSamplesDLInt1_v2/forager'
# newlyEmergedSWCPath = os.path.join('/home/ajay/PowerFolders/GinJangNDB_Upload/SigenSegmentations/Results',
#                                    'GoodSamplesDLInt1_v2', 'newlyEmerged')

foragerSWCPath = 'swcFiles/GoodSamplesDLInt1_v2/forager'

foragerNrns = ['HB130313-4NS_3ptSoma.swc',
               'HB130322-1NS_3ptSoma.swc',
               'HB130408-1NS_3ptSoma.swc',
               'HB130425-1NS_3ptSoma.swc',
               'HB130501-2NS_3ptSoma.swc',
               'HB060607-2NS_3ptSoma.swc'
                ]
cols = ['r', 'g', 'b', 'm', 'k', 'c', 'r', 'g']

foragerSWCs = [os.path.join(foragerSWCPath, x) for x in foragerNrns]

# foragerSWCs.append('swcFiles/HB060602_3ptSoma.swc')


# newlyEmergedNrns = ['HB130523-3NS_STD.swc', ]


for swcInd, swc in enumerate(foragerSWCs):
    [azPoints2D, bestTheta, ymin, xShift, err] = getAZ2D(swc)
    bestFitPts = rotatePts2D(np.asarray(azPoints2D), bestTheta)
    print ymin, xShift, err
    plt.plot(bestFitPts[:, 0] - xShift, bestFitPts[:, 1] - min(bestFitPts[:, 1]), cols[swcInd])

plt.draw()

# for swc in [os.path.join(newlyEmergedSWCPath, x) for x in newlyEmergedNrns]:
#     [azPoints2D, bestTheta, aPara, ymin, xShift, err] = getAZ2D(swc)
#     bestFitPts = rotatePts2D(np.asarray(azPoints2D), bestTheta)
#     print aPara, ymin, xShift, err
#     plt.plot(bestFitPts[:, 0] - xShift, bestFitPts[:, 1] - min(bestFitPts[:, 1]), 'b')
#
# plt.draw()

