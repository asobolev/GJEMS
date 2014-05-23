# from easygui import fileopenbox
import sys
from GJEMS.morph.morphImport import MorphImport
assert len(sys.argv) == 2, 'Only one argument, the path of the swcfile expected, ' + str(len(sys.argv)) + 'found'
testMorphFile = sys.argv[1]


testNrn = MorphImport(testMorphFile)
testNrn.initRegionIndices(testMorphFile.rstrip('.swc') + '.marks')
testNrn.saveSubtrees()

