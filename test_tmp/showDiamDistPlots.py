# import matplotlib.pyplot as plt
import sys
from GJEMS.morph.morph import *

assert len(sys.argv) == 2, 'Only one argument, the path of the swcfile expected, ' + str(len(sys.argv)) + 'found'
testMorphFile = sys.argv[1]

testMorph = BasicMorph(morphFile=testMorphFile)
testMorph.daimDistPlot()