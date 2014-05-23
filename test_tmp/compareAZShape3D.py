import os
import subprocess
import json

import matplotlib.pyplot as plt

from GJEMS.morph.morph import rotatePts2D, plotPoints3D, addPoints3D


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



def getAZ3D(swcFile):
    output = subprocess.check_output(['python', 'getAZ3D.py', swcFile])
    startStr = 'startJSON'
    return json.loads(output[output.find(startStr) + len(startStr): -1])




foragerSWCPath = '/home/ajay/PowerFolders/GinJangNDB_Upload/SigenSegmentations/Results/GoodSamplesDLInt1/forager'
newlyEmergedSWCPath = os.path.join('/home/ajay/PowerFolders/GinJangNDB_Upload/SigenSegmentations/Results',
                                   'GoodSamplesDLInt1', 'newlyEmerged')


fig = plt.figure()
plt.show(block=False)

foragerNrns = ['HB130313-4NS_3ptSoma_STD.swc',
               'HB130322-1NS_STD.swc',
               'HB130408-1NS_3ptSoma_STD.swc',
               'HB130425-1NS_STD.swc',
               'HB130501-2NS_STD.swc']

# foragerSWCs.append('/home/ajay/repos/GJEMS/test_tmp/swcFiles/HB060602_3ptSoma.swc')


newlyEmergedNrns = ['HB130523-3NS_STD.swc', ]



ax = plotPoints3D(fig, None)

for swc in foragerNrns:

    azPtsSTD = getAZ3D(os.path.join(foragerSWCPath, swc))
    addPoints3D(ax, azPtsSTD, 'r')

plt.draw()

for swc in newlyEmergedNrns:
    azPtsSTD = getAZ3D(os.path.join(newlyEmergedSWCPath, swc))
    addPoints3D(ax, azPtsSTD, 'b')

plt.draw()

