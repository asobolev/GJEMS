"""
Author: Ajayrama Kumaraswamy, LMU, Muenchen
Date: 26th Mar 2014
Version: 0.2

Changelog:
v0.2:
    i. This script will retain the header of the input file in the output file.
    ii. For Columns 3-6, ascii float format changed from 12 decimal points(%0.12f) to 3 decimalpoints(%0.3f)

Documentation:
This script takes the filepath of a swcfile(relative or absolute) and generates an swc file with the following changes:

  a. Converts root section into a three point section. Implementation taken from:  http://neuromorpho.org/neuroMorpho/SomaFormat.html

            1 1 xs ys rs -1

        is replaced by

            1 1 xs ys zs rs -1
            2 1 xs (ys-rs) zs rs 1
            3 1 xs (ys+rs) zs rs 1

  b. labels all other points as type '3'(in column 2)

If input is 'neuron.swc' then output is 'neuron_3ptSoma.swc'
"""

import numpy as npy
import sys

assert len(sys.argv) == 2, 'Only one argument, the path of the swcfile expected, ' + str(len(sys.argv)) + 'found'
fName = sys.argv[1]

headr = ''
with open(fName, 'r') as fle:
    lne = fle.readline()
    while lne[0] == '#':
        headr = headr + lne[1:]
        lne = fle.readline()


headr = headr.rstrip('\n')


inFile = npy.loadtxt(fName)

nPts = npy.shape(inFile)[0]
nChildPerPt = [0] * nPts
deletePt = [False] * nPts

for pt in inFile:

    if not pt[6] == -1:
        nChildPerPt[int(pt[6]) - 1] += 1

for ptInd in reversed(range(nPts)):

    if (nChildPerPt[ptInd] == 0) and (nChildPerPt[int(inFile[ptInd, 6]) - 1] > 1):

            deletePt[ptInd] = True






outFile = inFile[0, :].copy()
outFile[1] = 1

rs = inFile[0, 5] #radius of one-point soma


outFile = npy.vstack((outFile, npy.array([2, 1, inFile[0, 2], inFile[0, 3] - rs, inFile[0, 4], rs, 1])))
outFile = npy.vstack((outFile, npy.array([3, 1, inFile[0, 2], inFile[0, 3] + rs, inFile[0, 4], rs, 1])))

inParentVals = inFile[:, 6]

newIndices = npy.zeros([nPts, 1])
newIndices[0] = 1
ptsDone = 3

for lineId in range(1, inFile.shape[0]):

    if not deletePt[lineId]:

        presLine = inFile[lineId, :].copy()

        newIndices[lineId] = ptsDone + 1

        presLine[0] = ptsDone + 1

        if not presLine[6] == 1:	#points connected to the original single-point soma remains connected to same original point.
            presLine[6] = newIndices[int(presLine[0]) - 1]

        if not (presLine[1] == 3):
            presLine[1] = 3

        outFile = npy.vstack((outFile, presLine))

        ptsDone += 1

npy.savetxt(fName[:fName.index('.')]+'_3ptSoma.swc',outFile,'%d %d %0.3f %0.3f %0.3f %0.3f %d',
            header=headr, comments='#')