from easygui import fileopenbox

from GJEMS.morph.morph import BasicMorph


swcFile = fileopenbox(msg='SWC file with three point soma', filetypes=['*.swc'])
print 'Opening ',swcFile
testMorph = BasicMorph(swcFile)

#testMorph = BasicMorph('../swcFiles/HB130313-4NS_3ptSoma.swc')

