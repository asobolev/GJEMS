from GJEMS.morph.morph import BasicMorph, plotPoints3D, addPoints3D
import matplotlib.pyplot as pyplot
from easygui import fileopenbox

testMorphFile = fileopenbox(msg='SWC file with three point soma', filetypes=['*.swc'])
#testMorphFile = 'swcFiles/HB060602_3ptSoma.swc'
testMorph = BasicMorph(morphFile=testMorphFile)
azSecPtrs = testMorph.getActiveZoneSectionPtrs()
azSecPts, azDiam = testMorph.getActiveZonePoints(azSecPtrs)
azPointsInPlane, azPoints2D, evecs, svals = testMorph.project2plane(azSecPts)
ax = plotPoints3D(azSecPts)
addPoints3D(ax, azPointsInPlane)
