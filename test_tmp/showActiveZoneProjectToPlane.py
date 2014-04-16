from GJEMS.morph.morph import BasicMorph, rotatePts2D
import matplotlib.pyplot as plt
from easygui import fileopenbox
import numpy as np
from math import pi as PI
from math import sin, cos
from time import sleep

testMorphFile = fileopenbox(msg='SWC file with three point soma', filetypes=['*.swc'])
#testMorphFile = 'swcFiles/HB060602_3ptSoma.swc'



testMorph = BasicMorph(morphFile=testMorphFile)
azSecPtrs = testMorph.getActiveZoneSectionPtrs()
azSecPts, azDiam = testMorph.getActiveZonePoints(azSecPtrs)
azPointsInPlane, azPoints2D, evecs, svals = testMorph.project2plane(azSecPts)


# ax = testMorph.plotPoints3D(azSecPts, 'r-x')
# testMorph.addPoints3D(ax, azPointsInPlane, 'b-*')
# cols = ['r', 'b', 'g']
# mu = azSecPts.mean(axis=0)
# for evec, col in zip(evecs.T, cols):
#     vecPts = np.zeros([2, 3])
#     vecPts[0, :] = mu - 10 * evec / np.linalg.norm(evec)
#     vecPts[1, :] = mu + 10 * evec / np.linalg.norm(evec)
#     testMorph.addPoints3D(ax, vecPts, col + '-')

fig1 = plt.figure()
plt.show(block=False)

plt.plot(azPoints2D[:, 0], azPoints2D[:, 1], 'g-x')



# fig2 = plt.figure()
# plt.show(block=False)
# plt.plot(thetas, diffs)
# plt.draw()

plt.figure(fig1.number)

bestTheta, aPara, ymin, xShift,err  = testMorph.fitParabola(azPoints2D)
bestPts = rotatePts2D(azPoints2D, bestTheta)
yPara = ymin + aPara * ((bestPts[:, 0] - xShift) ** 2)

plt.plot(bestPts[:, 0] - xShift, bestPts[:, 1], 'r-x')
plt.plot(bestPts[:, 0] - xShift, yPara, 'b-')
plt.draw()

