import sys
import json

from GJEMS.morph.morph import BasicMorph


assert len(sys.argv) == 2, 'Only one argument, the path of the swcfile expected, ' + str(len(sys.argv)) + 'found'
swcfName = sys.argv[1]
testMorph = BasicMorph(swcfName)
azSecPtrs = testMorph.getActiveZoneSectionPtrs()
azSecPts, azDiam = testMorph.getActiveZonePoints(azSecPtrs)
azPointsInPlane, azPoints2D, evecs, svals = testMorph.project2plane(azSecPts)
bestTheta, aPara, ymin, xShift, err  = testMorph.fitParabola(azPoints2D)
print 'startJSON' + json.dumps([azPoints2D.tolist(), bestTheta, aPara, ymin, xShift, err])