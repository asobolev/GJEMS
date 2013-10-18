import sys

sys.path.append('../lib')

from morphImport import MorphImport

testMorphFile = '../swcFiles/HB060602_3ptSoma.swc'
testNrn = MorphImport(testMorphFile)
