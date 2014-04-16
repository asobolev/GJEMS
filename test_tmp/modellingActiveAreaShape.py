from easygui import fileopenbox

import numpy as np

from GJEMS.morph.morph import BasicMorph, rotatePts3D, rotatePts2D, addPoints3D, plotPoints3D


defaultPath = '/home/ajay/PowerFolders/GinJangNDB_Upload/SigenSegmentations/Results/GoodSamplesDLInt1/forager/*.swc'
testMorphFile = fileopenbox(msg='SWC file with three point soma', default=defaultPath)
# testMorphFile = 'swcFiles/HB060602_3ptSoma.swc'



testMorph = BasicMorph(morphFile=testMorphFile)
swcData = np.loadtxt(testMorphFile)
swcXYZ = swcData[:, 2:5]
azSecPtrs = testMorph.getActiveZoneSectionPtrs()
azSecPts = testMorph.getActiveZonePoints(azSecPtrs)
stdFunc = testMorph.getStandardizationFunction()
swcSTD = stdFunc(swcXYZ)
ax = plotPoints3D(swcSTD, 'rx')




