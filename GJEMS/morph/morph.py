import math
import os
from math import cos, sin
from math import pi as PI

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

from GJEMS.morph.morphImport import MorphImport, SubTreeWriter



#***********************************************************************************************************************

def rotatePts2D(pts, theta):
    rotMatrix = np.asarray([[cos(theta), -sin(theta)], [sin(theta), cos(theta)]])
    return np.dot(rotMatrix, pts.T).T

#***********************************************************************************************************************


def rotatePts3D(pts, rotMatrix):

    return np.dot(rotMatrix, pts.T).T

#***********************************************************************************************************************


def plotPoints3D(xyz, pltStr='x-r'):

    fig = plt.figure()
    plt.show(block=False)
    ax = fig.add_subplot(111, projection='3d')
    if xyz is not None:
        xyz = np.asarray(xyz)
        ax.plot(xyz[:,0], xyz[:,1], xyz[:,2], pltStr)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.draw()
    return ax

    #*******************************************************************************************************************


def addPoints3D(ax, xyz, pltStr='*-b'):

    xyz = np.asarray(xyz)
    ax.plot(xyz[:, 0], xyz[:, 1], xyz[:, 2], pltStr)
    plt.draw()

    #*******************************************************************************************************************

def getPCADetails(swcFileName):

    data = np.loadtxt(swcFileName)[:,2:5]
    mu = np.mean(data, axis=0)
    data = data - mu
    evec, eval, v = np.linalg.svd(data.T, full_matrices=False)
    dataProj = np.dot(data, evec)
    newStds = np.std(dataProj, axis=0)
    return evec, newStds

#***********************************************************************************************************************


class BasicMorph(MorphImport):

    lmio = None

    #*******************************************************************************************************************

    def __init__(self, morphFile, initDists=False):

        MorphImport.__init__(self, morphFile=morphFile)

        if initDists:
            self.initDistances()

    #*****************************************************************************************************************

    def rect2polar3D1Pt(self, pt):

        r = math.sqrt(pt[0] ** 2 + pt[1] ** 2 + pt[2] ** 2)
        theta = math.acos(pt[2] / r)
        phi = math.atan(pt[1] / pt[0])

        return r, theta, phi

    #*****************************************************************************************************************

    def getTipSperical(self):

        tipSpherical = []
        tempTree = SubTreeWriter(self.rootPtr)

        for secPtr in self.tipPtrs:

            xyzd = tempTree.getSectionxyzd(secPtr)

            tipSpherical.append(self.rect2polar3D1Pt(xyzd[len(xyzd) - 1][:3]))

        return np.array(tipSpherical)

    #*****************************************************************************************************************

    def getTipUV(self):

        tipUV = []
        tempTree = SubTreeWriter(self.rootPtr)

        for secPtr in self.tipPtrs:

            xyzd = tempTree.getSectionxyzd(secPtr)

            tipUV.append(self.rect2UV1Pt(xyzd[len(xyzd) - 1][:3]))

        return np.array(tipUV)

    #*****************************************************************************************************************

    def rect2UV1Pt(self, rectCoor):
        '''
        Reference : http://en.wikipedia.org/wiki/UV_mapping
        :param rectCoor:
        :return:
        '''

        unitVector = [x / math.sqrt(np.dot(rectCoor, rectCoor)) for x in rectCoor]

        u = 0.5 + math.atan2(unitVector[2], unitVector[0]) / 2 / math.pi

        v = 0.5 - math.asin(unitVector[1]) / math.pi\

        return u, v

    #*****************************************************************************************************************

    def accumulateSections(self, parentAcc, secPtr, stopSec):


        if secPtr.nchild() == 0:

            return []

        elif secPtr.sec == stopSec:

            presAccu = list(parentAcc)
            presAccu.append(secPtr)
            return presAccu

        else:

            presAccu = list(parentAcc)
            presAccu.append(secPtr)

            for childId in range(int(secPtr.nchild())):

                childPtr = self.getPtr(secPtr.child[childId])
                returnedAcc = self.accumulateSections(presAccu, childPtr, stopSec)

                if len(returnedAcc) > 0:
                    return returnedAcc

            return []

    #*****************************************************************************************************************

    def getActiveZoneSectionPtrs(self):

        self.initRegionIndices(os.path.join(self.morphFilePath, self.morphFileName.rstrip('.swc') + '.marks'))

        activeZoneSections = []

        for regionMarksSec in self.regionMarkSecs:
            activeZoneSections.append(self.accumulateSections([], self.rootPtr, regionMarksSec))

        return activeZoneSections

    #*****************************************************************************************************************

    def getActiveZonePoints(self, activeZoneSectionPtrs):

        azPoints = []
        azDiam = []


        for secPtr in reversed(activeZoneSectionPtrs[0][1:]):

            xyzds = self.getSectionxyzd(secPtr)

            for xyzd in reversed(xyzds[1:]):
                azPoints.append(xyzd[:3])
                azDiam.append(xyzd[3])

        azPoints.append(self.getSectionxyzd(self.rootPtr)[0][:3])
        azDiam.append(self.getSectionxyzd(self.rootPtr)[0][3])

        for secPtr in activeZoneSectionPtrs[1][1:]:

            xyzds = self.getSectionxyzd(secPtr)

            for xyzd in xyzds[1:]:
                azPoints.append(xyzd[:3])
                azDiam.append(xyzd[3])

        return np.asarray(azPoints), azDiam

    #*******************************************************************************************************************

    def project2plane(self, points):

        mu = np.mean(points, axis=0)
        centeredPoints = points - mu

        evecs, svals, v = np.linalg.svd(centeredPoints.T, full_matrices=False)

        planeVecs = np.matrix(evecs[:,:2])
        A = planeVecs   #defining an alias
        ATAinv = np.linalg.inv(A.T * A)
        projMatrix = A * ATAinv * A.T
        ptsInPlane = np.asarray(np.dot(projMatrix, centeredPoints.T).T)
        ptsIn2D = np.asarray(np.dot(A.T, centeredPoints.T).T)
        # from math import atan2, cos, sin
        # theta = atan2(np.mean(ptsIn2D[:, 1]), -np.mean(ptsIn2D[:, 0]))
        # rotMatrix = np.asarray([[cos(theta), -sin(theta)], [sin(theta), cos(theta)]])
        # ptsIn2D = np.dot(rotMatrix, ptsIn2D.T).T
        return ptsInPlane + mu, ptsIn2D, evecs, svals

    #*******************************************************************************************************************

    def getPCARotMatrix(self, points):

        mu = np.mean(points, axis=0)
        centeredPoints = points - mu

        evecs, svals, v = np.linalg.svd(centeredPoints.T, full_matrices=False)

        return evecs.T

    #*******************************************************************************************************************

    def getStandardizationFunction(self):

        azSecPtrs = self.getActiveZoneSectionPtrs()
        azSecPts, azDiam = self.getActiveZonePoints(azSecPtrs)
        rotMatrix = self.getPCARotMatrix(azSecPts)
        azPointsInPlane, azPoints2D, evecs, svals = self.project2plane(azSecPts)
        bestTheta, aPara, ymin, xShift, err = self.fitParabola(azPoints2D)
        azPointsPCARot = rotatePts3D(azSecPts, rotMatrix)
        azSecPts2DRot = rotatePts2D(azPoints2D, bestTheta)
        #The rotation matrix is defined assuming origin at the mean point of the AZ points. So, the whole neuron must
        #be moved, so that the the origin is at the mean point of the AZ points.
        xyzShift1 = np.mean(azSecPts, axis=0)
        #After applying the two rotations, final adjustments to bring the apex of the parabola to (0, 0, 0)
        xyzShift2 = np.asarray([xShift, min(azSecPts2DRot[:, 1]), 0])

        def standardize(pts, rotMatrix=rotMatrix, bestTheta=bestTheta, xyzShift1=xyzShift1, xyzShift2=xyzShift2):

            pts -= xyzShift1
            azPtsRotPCA = rotatePts3D(pts, rotMatrix)
            azPtsStandard = np.zeros(np.shape(azPtsRotPCA))
            azPtsStandard[:, 2] = azPtsRotPCA[:, 2]
            azPtsStandard[:, :2] = rotatePts2D(azPtsRotPCA[:, :2], bestTheta)
            azPtsStandard -= xyzShift2

            return azPtsStandard

        return standardize

    #*******************************************************************************************************************

    def fitParabola(self, pts):

        diffs = []
        thetas = np.linspace(0, 2 * PI, 500)
        ymins = []
        aParas = []
        xShifts = []
        tempFig = plt.figure()
        plt.show(block = False)
        for theta in thetas:
            xWhenyIs0 = []
            ptsIn2DRot = rotatePts2D(pts, theta)
            transitionInds = []
            for ind in range(len(ptsIn2DRot) - 1):
                if not np.signbit(ptsIn2DRot[ind, 1]) == np.signbit(ptsIn2DRot[ind + 1, 1]):
                    xWhenyIs0.append(np.mean(ptsIn2DRot[ind: ind + 2, 0]))
                    transitionInds.append(ind)
            if not len(xWhenyIs0) in [2, 3, 4]:

                diffs.append(1e6)
                ymins.append(0)
                aParas.append(0)
                xShifts.append(0)

            else:
                xStart = transitionInds[0]
                xStop = transitionInds[-1]
                if xStart > xStop:
                    temp = xStop
                    xStop = xStart
                    xStart = temp

                xNegMean = np.mean(xWhenyIs0[xWhenyIs0 < 0])
                xPosMean = np.mean(xWhenyIs0[xWhenyIs0 > 0])
                xShift = 0.5 * (xPosMean + xNegMean)

                if (xStop - xStart) < 0.3 * len(pts):

                    diffs.append(1e6)
                    ymins.append(0)
                    aParas.append(0)
                    xShifts.append(0)

                else:
                    xtoFit = ptsIn2DRot[xStart: xStop + 1, 0] - xShift
                    ytoFit = ptsIn2DRot[xStart: xStop + 1, 1]

                    # xtoFit = ptsIn2DRot[:, 0] - xShift
                    # ytoFit = ptsIn2DRot[:, 1]

                    xAxisIntercept = 0.5 * (xPosMean - xNegMean)
                    ymin = min(ptsIn2DRot[:, 1])
                    #compare with a parabola given by: y - ymin = a * x**2
                    aPara = -ymin / (xAxisIntercept ** 2)

                    yPara = ymin + aPara * (xtoFit ** 2)

                    aParas.append(aPara)
                    ymins.append(ymin)
                    xShifts.append(xShift)

                    diffs.append(np.linalg.norm(yPara - ytoFit))

                   # if diffs[-1] < 80:
                    #     plt.cla()
                    #     plt.plot(ptsIn2DRot[:, 0], ptsIn2DRot[:, 1], 'b')
                    #     plt.plot(xtoFit, ytoFit, 'g')
                    #     plt.plot(xtoFit, yPara, 'r')
                    #     plt.draw()
                    #     print diffs[-1], len(xWhenyIs0), theta * 180 / PI
                    #     import ipdb
                    #     ipdb.set_trace()



        # plt.figure(tempFig.number)
        # plt.plot(thetas * 180 / PI, diffs)
        # plt.ylim([0, 100])
        # plt.draw()
        # import ipdb
        # ipdb.set_trace()

        bestInd = np.argmin(diffs)

        return thetas[bestInd], aParas[bestInd], ymins[bestInd], xShifts[bestInd], diffs[bestInd]

#***********************************************************************************************************************

