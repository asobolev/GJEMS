import math
from GJEMS.morphImport import MorphImport, SubTreeWriter
from LMIO.wrapper import LMIO
# import matplotlib.pyplot as plt
import numpy as np

#***********************************************************************************************************************

def getPCADetails(swcFileName):

    data = np.loadtxt(swcFileName)[:,2:5]
    mu = np.mean(data, axis=0)
    data = data - mu
    evec, eval,v = np.linalg.svd(data.T, full_matrices=False)
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

#***********************************************************************************************************************
