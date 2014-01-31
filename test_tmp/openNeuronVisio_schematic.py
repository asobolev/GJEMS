from GJEMS.morph import BasicMorph
from neuronvisio.controls import Controls
from easygui import fileopenbox


testMorph = BasicMorph(fileopenbox(msg='SWC file with three point soma', filetypes=['*.swc']))

for secs in testMorph.allsec:
    secs.diam = 1

#testMorph = BasicMorph('../swcFiles/HB130313-4NS_3ptSoma.swc')

contols = Controls()