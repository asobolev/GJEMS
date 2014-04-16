from GJEMS.morph.morph import BasicMorph, rotatePts3D
import sys
import numpy as np

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
standFunc = testMorph.getStandardizationFunction()
swcData[:, 2:5] = standFunc(swcData[:, 2:5])



np.savetxt(swcfName[:swcfName.index('.')]+'_STD.swc', swcData,'%d %d %0.6f %0.6f %0.6f %0.6f %d',
            header=headr, comments='#')