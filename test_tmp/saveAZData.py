from GJEMS.morph.morph import BasicMorph
import sys
import numpy as np

assert len(sys.argv) == 2, 'Only one argument, the path of the swcfile expected, ' + str(len(sys.argv)) + 'found'
swcfName = sys.argv[1]

testMorph = BasicMorph(swcfName)
azSecPtrs = testMorph.getActiveZoneSectionPtrs()
azSecPts, azDiam = testMorph.getActiveZonePoints(azSecPtrs)
toSave = np.zeros([np.shape(azSecPts)[0], 4])
toSave[:, :3] = azSecPts
toSave[:, 3] = azDiam
np.savetxt(swcfName.rstrip('.swc') + '.AZData', toSave, '%0.3f')