from neuronvisio.controls import Controls
import sys
from GJEMS.morph.morph import BasicMorph

assert len(sys.argv) == 2, 'Only one argument, the path of the swcfile expected, ' + str(len(sys.argv)) + 'found'
swcfName = sys.argv[1]
testMorph = BasicMorph(swcfName)

for secs in testMorph.allsec.values():
    secs.diam = 1

#testMorph = BasicMorph('../swcFiles/HB130313-4NS_3ptSoma.swc')

contols = Controls()
