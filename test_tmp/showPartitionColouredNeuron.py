from GJEMS.morph.morphImport import MorphImport
from easygui import fileopenbox
import neuron as nrn
import sys
import os

# testMorphFile = 'swcFiles/HB060602_3ptSoma_subTrees/HB060602_3ptSoma_db.swc'
testMorphFile = fileopenbox(msg='SWC file with three point soma', filetypes=['*.swc'])
# assert len(sys.argv) == 2, 'Only one argument, the path of the swcfile expected, ' + str(len(sys.argv)) + 'found'
# testMorphFile = os.path.abspath(sys.argv[1])
testNrn = MorphImport(testMorphFile)
testNrn.initRegionIndices(testMorphFile.rstrip('.swc') + '.marks')
from neuron import gui
fig = nrn.h.PlotShape()
fig.variable('index_regionInd')
fig.exec_menu('Shape Plot')
fig.scale(0, 3)
fig.show(0)
fig.flush()
