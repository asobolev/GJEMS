# from easygui import fileopenbox
import sys
from GJEMS.morph.morph import BasicMorph

assert len(sys.argv) == 2, 'Only one argument, the path of the swcfile expected, ' + str(len(sys.argv)) + 'found'
swcFile = sys.argv[1]
# swcFile = fileopenbox(msg='SWC file with three point soma', filetypes=['*.swc'])
print 'Opening ',swcFile
testMorph = BasicMorph(swcFile)

#testMorph = BasicMorph('../swcFiles/HB130313-4NS_3ptSoma.swc')

from neuron import gui