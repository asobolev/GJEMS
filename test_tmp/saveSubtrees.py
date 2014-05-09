# from easygui import fileopenbox
import sys
from GJEMS.morph.morphImport import MorphImport
from matplotlib import pyplot as plt
import numpy as np

assert len(sys.argv) == 2, 'Only one argument, the path of the swcfile expected, ' + str(len(sys.argv)) + 'found'
testMorphFile = sys.argv[1]
# testMorphFile = 'swcFiles/HB060602_3ptSoma_subTrees/HB060602_3ptSoma_db.swc'
# testMorphFile = fileopenbox(msg='SWC file with three point soma', filetypes=['*.swc'])
testNrn = MorphImport(testMorphFile)
testNrn.initRegionIndices(testMorphFile.rstrip('.swc') + '.marks')
testNrn.saveSubtrees()

# nChilds = []
# for sec in testNrn.allsec:
#     nChilds.append(testNrn.getPtr(sec).nchild())
#
# nChildHist, nChildBins = np.histogram(nChilds, np.arange(0.5, 6, 1))
#
# fig1 = plt.figure()
# plt.show(block=False)
# plt.plot(range(5), np.cumsum(nChildHist), 'ro', mfc='r', ms=5)
# plt.draw()

# controls = Controls()
