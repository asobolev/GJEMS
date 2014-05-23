import math
import os
from math import cos, sin
from math import pi as PI

import matplotlib.pyplot as plt
import numpy as np
import neuron as nrn

from GJEMS.morph.morphImport import MorphImport, SubTreeWriter


#***********************************************************************************************************************
def rotationMatrix(axis, theta):
    """
    Function taken verbatim from http://stackoverflow.com/questions/6802577/python-rotation-of-3d-vector.
    Returns a 3D rotation matrix corresponding to a counter-clockwise rotation to theta about axis.
    :param axis: 3 element np array
    :param theta: float
    :return: np array of shape (3, 3)
    """
    axis = axis/math.sqrt(np.dot(axis,axis))
    a = math.cos(theta/2)
    b, c, d = -axis*math.sin(theta/2)
    return np.array([[a*a+b*b-c*c-d*d, 2*(b*c-a*d), 2*(b*d+a*c)],
                     [2*(b*c+a*d), a*a+c*c-b*b-d*d, 2*(c*d-a*b)],
                     [2*(b*d-a*c), 2*(c*d+a*b), a*a+d*d-b*b-c*c]])

#***********************************************************************************************************************

def rotatePts2D(pts, theta):
    rotMatrix = np.asarray([[cos(theta), -sin(theta)], [sin(theta), cos(theta)]])
    return np.dot(rotMatrix, np.asarray(pts).T).T

#***********************************************************************************************************************

def rotatePts3D(pts, rotMatrix):

    return np.dot(rotMatrix, np.asarray(pts).T).T

#***********************************************************************************************************************

def getRotMatWithStartTargetVector(start, target):
    angle = math.acos(np.dot(target, start))
    axis = np.cross(target, start)
    return rotationMatrix(axis, angle)

#***********************************************************************************************************************

def plotPoints3D(fig, xyz, pltStr='x-r', subplot=111):

    ax = fig.add_subplot(subplot, projection='3d')
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

def getPCADetails(swcFileName, center=True):

    data = np.loadtxt(swcFileName)[:,2:5]
    if center:
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

        for sec in self.allsec.values():
            sec.push()
            sec.nseg = int(nrn.h.n3d()) - 1
            nrn.h.pop_section()

        if initDists:
            self.initDistances()

    #*****************************************************************************************************************

    def rect2polar3D1Pt(self, pt):

        r = math.sqrt(pt[0] ** 2 + pt[1] ** 2 + pt[2] ** 2)
        theta = math.acos(pt[2] / r)
        phi = math.atan(pt[1] / pt[0])

        return [r, theta, phi]

    #*****************************************************************************************************************

    def polar2rect3D1Pt(self, pt):

        x = pt[0] * math.sin(pt[1] * math.cos(pt[2]))
        y = pt[0] * math.sin(pt[1] * math.sin(pt[2]))
        z = pt[0] * math.cos(pt[1])

        return [x, y, z]

    #*****************************************************************************************************************

    def getTipSpherical(self):

        tipSpherical = []

        for secPtr in self.tipPtrs.values():

            if secPtr.sec.nseg > 2:

                xyzr = self.getSectionxyzr(secPtr)

                tipSpherical.append(self.rect2polar3D1Pt(xyzr[len(xyzr) - 1][:3]))

        return np.array(tipSpherical)

    #*****************************************************************************************************************

    def getTipUVOpenX(self):

        tipUV = []
        actualRadii = []

        for secPtr in self.tipPtrs.values():

            if secPtr.sec.nseg > 2:

                xyzr = self.getSectionxyzr(secPtr)

                tipUV.append(self.rect2UV1Pt(xyzr[-1][:3]))
                actualRadii.append(np.linalg.norm(xyzr[-1][:3]))

        return [tipUV, actualRadii]

    #*****************************************************************************************************************

    def getTipUVOpenY(self):

        tipUV = []
        actualRadii = []

        for secPtr in self.tipPtrs.values():

            if secPtr.sec.nseg > 2:

                xyzr = self.getSectionxyzr(secPtr)
                rotXYZ = np.hstack((rotatePts2D(xyzr[-1][:2], PI / 2), xyzr[-1][2]))

                tipUV.append(self.rect2UV1Pt(rotXYZ))
                actualRadii.append(np.linalg.norm(xyzr[-1][:3]))

        return [tipUV, actualRadii]

    #*****************************************************************************************************************

    def getTipXYZ(self):

        tipXYZ = []

        for secPtr in self.tipPtrs.values():

            if secPtr.sec.nseg > 2:

                xyzr = self.getSectionxyzr(secPtr)
                tipXYZ.append(xyzr[-1][:3])

        return tipXYZ

    #****************************************************************************************************************


    def rect2UV1Pt(self, rectCoor):
        '''
        Reference : http://en.wikipedia.org/wiki/UV_mapping
        :param rectCoor:
        :return:
        '''

        unitVector = rectCoor / np.linalg.norm(rectCoor)

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

            xyzrs = self.getSectionxyzr(secPtr)

            for xyzr in reversed(xyzrs[1:]):
                azPoints.append(xyzr[:3])
                azDiam.append(xyzr[3])

        azPoints.append(self.getSectionxyzr(self.rootPtr)[0][:3])
        azDiam.append(self.getSectionxyzr(self.rootPtr)[0][3])

        for secPtr in activeZoneSectionPtrs[1][1:]:

            xyzrs = self.getSectionxyzr(secPtr)

            for xyzr in xyzrs[1:]:
                azPoints.append(xyzr[:3])
                azDiam.append(xyzr[3])

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

        return ptsInPlane + mu, ptsIn2D, evecs, svals

    #*******************************************************************************************************************

    def getPCARotMatrix(self, points, center=True):

        if center:
            mu = np.mean(points, axis=0)
            points = points - mu

        evecs, svals, v = np.linalg.svd(points.T, full_matrices=False)

        return evecs.T

    #*******************************************************************************************************************

    def getAllPts(self):

        return np.loadtxt(os.path.join(self.morphFilePath, self.morphFileName))[:, 2:5]

    #*******************************************************************************************************************

    def getStdFunctionPCA(self):

        azSecPtrs = self.getActiveZoneSectionPtrs()
        azSecPts, azDiam = self.getActiveZonePoints(azSecPtrs)
        rotMatrix = self.getPCARotMatrix(azSecPts)
        azPointsInPlane, azPoints2D, evecs, svals = self.project2plane(azSecPts)
        bestTheta, ymin, xShift, err = self.symmetrySearchByRotation(azPoints2D)
        azPointsPCARot = rotatePts3D(azSecPts, rotMatrix)
        azSecPts2DRot = rotatePts2D(azPoints2D, bestTheta)


        AZMean = np.mean(azSecPts, axis=0)
        allPts = self.getAllPts()


        actualUApex = np.hstack((rotatePts2D([xShift, min(azSecPts2DRot[:, 1])], -bestTheta), 0))
        actualUApex = rotatePts3D(actualUApex, rotMatrix.T) + AZMean
        rotMatrix1 = self.getPCARotMatrix(allPts - actualUApex, center=False)


        def standardize(pts, xyzShift=actualUApex, rotMatrix=rotMatrix1):

            pts -= xyzShift
            return rotatePts3D(pts, rotMatrix)

        return standardize

    #*******************************************************************************************************************

    def getStdFunctionPCA1(self):

        azSecPtrs = self.getActiveZoneSectionPtrs()
        azSecPts, azDiam = self.getActiveZonePoints(azSecPtrs)
        rotMatrix = self.getPCARotMatrix(azSecPts)
        azPointsInPlane, azPoints2D, evecs, svals = self.project2plane(azSecPts)
        bestTheta, ymin, xShift, err = self.symmetrySearchByRotation(azPoints2D)
        azPointsPCARot = rotatePts3D(azSecPts, rotMatrix)
        azSecPts2DRot = rotatePts2D(azPoints2D, bestTheta)


        AZMean = np.mean(azSecPts, axis=0)
        allPts = self.getAllPts()


        actualUApex = np.hstack((rotatePts2D([xShift, min(azSecPts2DRot[:, 1])], -bestTheta), 0))
        actualUApex = rotatePts3D(actualUApex, rotMatrix.T) + AZMean
        evecs, evals, v = np.linalg.svd((allPts - actualUApex).T, full_matrices=False)
        rotMatrix1 = getRotMatWithStartTargetVector(evecs[:, 0], [1, 0, 0])


        def standardize(pts, xyzShift=actualUApex, rotMatrix=rotMatrix1):

            pts -= xyzShift
            return rotatePts3D(pts, rotMatrix)

        return standardize

    #*******************************************************************************************************************

    def getStdFunctionUAlign(self):

        azSecPtrs = self.getActiveZoneSectionPtrs()
        azSecPts, azDiam = self.getActiveZonePoints(azSecPtrs)
        rotMatrix = self.getPCARotMatrix(azSecPts)
        azPointsInPlane, azPoints2D, evecs, svals = self.project2plane(azSecPts)
        bestTheta, ymin, xShift, err = self.symmetrySearchByRotation(azPoints2D)

        azSecPts2DRot = rotatePts2D(azPoints2D, bestTheta)

        AZMean = np.mean(azSecPts, axis=0)
        rotUMean = np.asarray([xShift, min(azSecPts2DRot[:, 1]), 0])


        def standardize(pts, rotMatrix=rotMatrix, bestTheta=bestTheta, xyzShift1=AZMean, xyzShift2=rotUMean):

            pts -= xyzShift1
            azPtsRotPCA = rotatePts3D(pts, rotMatrix)
            azPtsStandard = np.zeros(np.shape(azPtsRotPCA))
            azPtsStandard[:, 2] = azPtsRotPCA[:, 2]
            azPtsStandard[:, :2] = rotatePts2D(azPtsRotPCA[:, :2], bestTheta)
            azPtsStandard -= xyzShift2
            azPtsStandard[:, :2] = rotatePts2D(azPtsStandard[:, :2], -PI / 2)

            return azPtsStandard

        return standardize

    #*******************************************************************************************************************
    def symmetrySearchByRotation(self, pts):

        diffs = []
        thetas = np.linspace(0, 2 * PI, 500)
        ymins = []
        aParas = []
        xShifts = []
        # tempFig = plt.figure()
        # plt.show(block = False)
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
                xStart = min(transitionInds[0], transitionInds[-1])
                xStop = max(transitionInds[0], transitionInds[-1])
                xNegMean = np.mean(xWhenyIs0[xWhenyIs0 < 0])
                xPosMean = np.mean(xWhenyIs0[xWhenyIs0 > 0])
                xShift = 0.5 * (xPosMean + xNegMean)

                xtoFit = ptsIn2DRot[xStart: xStop + 1, 0] - xShift
                ytoFit = ptsIn2DRot[xStart: xStop + 1, 1]

                if ((xStop - xStart) < 0.3 * len(pts)) or (len(np.where(ytoFit > 0)[0]) > len(np.where(ytoFit < 0)[0])):
                # if len(np.where(ytoFit > 0)[0]) > len(np.where(ytoFit < 0)[0]):

                    diffs.append(1e6)
                    ymins.append(0)
                    aParas.append(0)
                    xShifts.append(0)

                else:

                    ymin = min(ytoFit)

                    # xtoFit = ptsIn2DRot[:, 0] - xShift
                    # ytoFit = ptsIn2DRot[:, 1]

                    # xAxisIntercept = 0.5 * (xPosMean - xNegMean)

                    # #compare with a parabola given by: y - ymin = a * x**2
                    # aPara = -ymin / (xAxisIntercept ** 2)

                    # yPara = ymin + aPara * (xtoFit ** 2)
                    # diff = np.linalg.norm(yPara - ytoFit)

                    interpN = 1000
                    xInterp = np.linspace(xtoFit[0], xtoFit[-1], interpN)
                    yinterp = np.interp(xInterp, xtoFit, ytoFit)
                    diff = np.abs(sum([yinterp[x] - yinterp[interpN - 1 - x] for x in range(int(interpN / 2))]) \
                           / (xPosMean - xNegMean))


                    # aParas.append(aPara)
                    ymins.append(ymin)
                    xShifts.append(xShift)

                    diffs.append(diff)

                    # if diffs[-1] < 5:
                    #     plt.cla()
                    #     plt.plot(ptsIn2DRot[:, 0], ptsIn2DRot[:, 1], 'b')
                    #     plt.plot(xtoFit, ytoFit, 'g')
                    #     # plt.plot(xtoFit, yPara, 'r')
                    #     plt.title(str([diffs[-1], len(xWhenyIs0), theta * 180 / PI]))
                    #     plt.draw()
                    #     import ipdb
                    #     ipdb.set_trace()



        # plt.figure(tempFig.number)
        # plt.plot(thetas * 180 / PI, diffs)
        # plt.ylim([0, 1])
        # plt.draw()
        # import ipdb
        # ipdb.set_trace()

        bestInd = np.argmin(diffs)

        return thetas[bestInd], ymins[bestInd], xShifts[bestInd], diffs[bestInd]

    #*******************************************************************************************************************

    def daimDistPlot(self):

        self.initDistances()

        fig = plt.figure()
        plt.show(block=False)
        ch='y'
        while not ch == 'q':

            ch = raw_input('Enter Dend number(\'q\' to quit):')

            chSec = self.allsec['Cell[0].dend[' + str(int(ch)) + ']']
            presentPtr = self.getPtr(chSec)

            diams = []
            dists = []
            sects = []
            while not presentPtr.root().sec.name() == presentPtr.sec.name():

                sects.append(presentPtr.sec)
                dists.extend([x for x in reversed(self.secdists[presentPtr.sec.name()])])
                diams.extend([x[3] for x in reversed(self.getSectionxyzr(presentPtr))])

                presentPtr = self.getPtr(presentPtr.parent().sec)

            plt.cla()
            # plt.plot(dists[:-1], np.diff(diams) / np.diff(dists), 'b')
            plt.plot(dists, diams, 'b')
            plt.title(chSec.name())
            plt.xlabel('EucDistance(um)')
            plt.ylabel('Diameter(um)')
            plt.draw()
            print [x.name()[13:-1] for x in sects]

            import ipdb
            ipdb.set_trace()

        plt.draw()
        return fig
    #*******************************************************************************************************************

    def initDistances(self):

        self.secdists = {}

        for secName, sec in self.allsec.iteritems():
            self.secdists[secName] = []
            sec.push()
            for pointInd in range(sec.nseg):
                self.secdists[secName].append(nrn.h.distance(pointInd * 1.0 / sec.nseg))
            nrn.h.pop_section()

    #*******************************************************************************************************************

    def getMeasure(self, f):

        measureDict = {}

        for secName, sec in self.allsec.iteritems():

            measureDict[secName] = []

            for ind in range(sec.nseg):

                measureDict.append(f(sec))

        return measureDict

#***********************************************************************************************************************