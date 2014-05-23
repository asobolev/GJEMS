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


newlyEmergedSWCPath = 'swcFiles/GoodSamplesDLInt1_v2/newlyEmerged'

newlyEmergedNrns = ['HB130523-3NS_3ptSoma.swc',
               'HB130605-1NS_3ptSoma.swc',
               'HB130605-2NS_3ptSoma.swc'
                ]
cols = ['r', 'g', 'b', 'm', 'k', 'c', 'r', 'g']

newlyEmergedSWCs = [os.path.join(newlyEmergedSWCPath, x) for x in newlyEmergedNrns]




for swcInd, swc in enumerate(newlyEmergedSWCs):
    [azPoints2D, bestTheta, ymin, xShift, err] = getAZ2D(swc)
    bestFitPts = rotatePts2D(np.asarray(azPoints2D), bestTheta)
    print ymin, xShift, err
    plt.plot(bestFitPts[:, 0] - xShift, bestFitPts[:, 1] - min(bestFitPts[:, 1]), cols[swcInd])

plt.draw()


