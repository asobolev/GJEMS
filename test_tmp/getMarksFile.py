# from easygui import fileopenbox
from GJEMS.morph.morphImport import MorphImport
import os
import numpy as np
import sys


def readRootSWC(swcFName, precision=3):
    """
    Reads and returns the root point of the swc file.
    :return:
    """
    with open(swcFName, 'r') as fle:
        line = fle.readline()
        while not line == '':
            if not line[0] == '#':
                entries = line.rstrip('\n').split(' ')
                # import ipdb
                # ipdb.set_trace()
                if entries[6] == '-1':
                    return [round(float(x), precision) for x in entries[:7]]

            line = fle.readline()

# swcFile = fileopenbox(msg='SWC file with three point soma', filetypes=['*.swc'])
assert len(sys.argv) == 2, 'Only one argument, the path of the swcfile expected, ' + str(len(sys.argv)) + 'found'
swcFile = sys.argv[1]
NRN = MorphImport(swcFile)


# partLabels = ['_DB', '_VB']
partLabels = ['-DB', '-VB']
partsDone = [False, False]
partRootDatas = [[] for x in partLabels]
partBoundarySections = [[] for x in partLabels]
compPres = 3

def getLabelSections(secPtr):

    xVals = np.asarray([x[2] for x in partRootDatas])
    sectionXYZD = NRN.getSectionxyzd(secPtr)
    for xyzd in sectionXYZD:

        whereXMatches = np.where(xVals == round(xyzd[0], compPres))[0]
        if len(whereXMatches):
            if not partsDone[whereXMatches]:
                if partRootDatas[whereXMatches][3] == round(xyzd[1], compPres):
                    if partRootDatas[whereXMatches][4] == round(xyzd[2], compPres):
                        partsDone[whereXMatches] = True
                        partBoundarySections[whereXMatches] = secPtr.sec
                        return

    for childInd in range(int(secPtr.nchild())):

        childPtr = NRN.getPtr(secPtr.child[childInd])
        getLabelSections(childPtr)

    return


swcFileName = swcFile.rstrip('.swc')

swcFileNameCore = swcFileName[:]
ptSoma = False
if swcFileName[-8:] == '_3ptSoma':
    ptSoma = True
    swcFileNameCore = swcFileName[:-8]

for partInd, partLabel in enumerate(partLabels):

    if not ptSoma:
        partRootDatas[partInd] = readRootSWC(swcFileNameCore + partLabel + '.swc')
    else:
        partRootDatas[partInd] = readRootSWC(swcFileNameCore + partLabel + '_3ptSoma.swc')


getLabelSections(NRN.rootPtr)

with open(swcFileName + '.marks', 'w') as fle:

    fle.write('#Section names to mark the beginings of different regions.\n\n'
              + '#SomaConnectionPoint\tdorsal\tventral\n')
    fle.write('Cell[0].dend[0]\t' + partBoundarySections[0].name() + '\t' + partBoundarySections[1].name())