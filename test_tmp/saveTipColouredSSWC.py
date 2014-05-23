from GJEMS.morph.morphImport import SubTreeWriter
from GJEMS.morph.morph import BasicMorph
import sys
import os

assert len(sys.argv) == 2, 'Only one argument, the path of the swcfile expected, ' + str(len(sys.argv)) + 'found'
testMorphFile = os.path.abspath(sys.argv[1])

def extraColFunc(secPtr):

    if secPtr.nchild():
        return [0]

    else:
        return [4 + secPtr.sec.nseg]

sswcFName = testMorphFile[:-4] + '_TipColoured.sswc'

NRN = BasicMorph(testMorphFile)
wri = SubTreeWriter(NRN.rootPtr, extraColFunc)
wri.write(sswcFName)