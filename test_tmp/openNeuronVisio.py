from GJMorphSim.morph import BasicMorph
from neuronvisio.controls import Controls
from easygui import fileopenbox


testMorph = BasicMorph(fileopenbox(msg='SWC file with single point soma', filetypes=['*.swc']))

#testMorph = BasicMorph('../swcFiles/HB130313-4NS_3ptSoma.swc')

contols = Controls()
