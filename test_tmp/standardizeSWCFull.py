from GJEMS.morph.morph import BasicMorph, rotatePts3D, getRotMatWithStartTargetVector
import sys
import numpy as np
import os
import shutil

assert len(sys.argv) == 2, 'Only one argument, the path of the swcfile expected, ' + str(len(sys.argv)) + 'found'
swcfName = sys.argv[1]

headr = ''
with open(swcfName, 'r') as fle:
    lne = fle.readline()
    while lne[0] == '#':
        headr = headr + lne[1:]
        lne = fle.readline()


headr = headr.rstrip('\n')

testMorph = BasicMorph(swcfName)
swcData = np.loadtxt(swcfName)

swcPts = swcData[:, 2:5]
# rotMatPCA = testMorph.getPCARotMatrix(swcPts)
# swcPts -= np.mean(swcPts, axis=0)
# swcData[:, 2:5] = rotatePts3D(swcPts, rotMatPCA)
standFunc = testMorph.getStdFunctionPCA()
swcData[:, 2:5] = standFunc(swcData[:, 2:5])

# evecs, evals, v = np.linalg.svd(swcData[:, 2:5].T, full_matrices=False)
#
# smallRot = getRotMatWithStartTargetVector(evecs[:, 0], [0, 1, 0])
#
# swcData[:, 2:5] = rotatePts3D(swcData[:, 2:5], smallRot)


np.savetxt(swcfName[:swcfName.index('.')]+'_FSTD.swc', swcData,'%d %d %0.6f %0.6f %0.6f %0.6f %d',
            header=headr, comments='#')

marksFilePath = swcfName[:-4] + '.marks'
if os.path.isfile(marksFilePath):
    shutil.copy(marksFilePath, swcfName[:-4] + '_FSTD.marks')