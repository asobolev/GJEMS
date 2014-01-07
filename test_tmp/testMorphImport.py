from GJMorphSim.morphImport import MorphImport
from neuronvisio.controls import Controls
from easygui import fileopenbox

# testMorphFile = 'swcFiles/HB060602_3ptSoma_subTrees/HB060602_3ptSoma_db.swc'
testMorphFile = fileopenbox(msg='SWC file with three point soma', filetypes=['*.swc'])
testNrn = MorphImport(testMorphFile)
testNrn.initRegionIndices(testMorphFile.rstrip('.swc') + '.marks')
testNrn.saveSubtrees()

from neuron import gui
# controls = Controls()
