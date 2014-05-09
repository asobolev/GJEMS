from GJEMS.morph.morph import BasicMorph, rotatePts2D
import matplotlib.pyplot as plt
# from easygui import fileopenbox
import sys

assert len(sys.argv) == 2, 'Only one argument, the path of the swcfile expected, ' + str(len(sys.argv)) + 'found'
testMorphFile = sys.argv[1]
# testMorphFile = fileopenbox(msg='SWC file with three point soma', filetypes=['*.swc'])
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
plt.draw()


# fig2 = plt.figure()
# plt.show(block=False)
# plt.plot(thetas, diffs)
# plt.draw()



bestTheta, ymin, xShift,err  = testMorph.symmetrySearchByRotation(azPoints2D)
bestPts = rotatePts2D(azPoints2D, bestTheta)
# yPara = ymin + aPara * ((bestPts[:, 0] - xShift) ** 2)

plt.figure(fig1.number)
plt.plot(bestPts[:, 0] - xShift, bestPts[:, 1], 'r-x')
# plt.plot(bestPts[:, 0] - xShift, yPara, 'b-')
plt.draw()

