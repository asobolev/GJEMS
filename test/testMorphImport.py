import sys

sys.path.append('../lib')

from morphImport import MorphImport
from neuronvisio.controls import Controls

testMorphFile = '../swcFiles/HB060602_3ptSoma.swc'
testNrn = MorphImport(testMorphFile)

from neuron import gui