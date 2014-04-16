from GJEMS.morph.morphImport import MorphImport
from neuronvisio.controls import Controls
from easygui import fileopenbox
import neuron as nrn

# testMorphFile = 'swcFiles/HB060602_3ptSoma_subTrees/HB060602_3ptSoma_db.swc'
testMorphFile = fileopenbox(msg='SWC file with three point soma', filetypes=['*.swc'])
testNrn = MorphImport(testMorphFile)
testNrn.initRegionIndices(testMorphFile.rstrip('.swc') + '.marks')
from neuron import gui
fig = nrn.h.PlotShape()
fig.variable('index_regionInd')
fig.exec_menu('Shape Plot')
fig.scale(0, 3)
fig.show(0)
fig.flush()
