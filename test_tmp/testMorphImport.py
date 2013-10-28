from GJMorphSim.morphImport import MorphImport
from neuronvisio.controls import Controls

# testMorphFile = 'swcFiles/HB060602_3ptSoma_subTrees/HB060602_3ptSoma_db.swc'
testMorphFile = 'swcFiles/HB060602_3ptSoma.swc'
testNrn = MorphImport(testMorphFile)
# self.initRegionIndices(morphFile.rstrip('.swc') + '.marks')
# testNrn.saveSubtrees()

# from neuron import gui
controls = Controls()
