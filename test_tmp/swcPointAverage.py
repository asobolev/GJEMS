import numpy as np
from easygui import fileopenbox
import math
from GJEMS.morph.morph import rotatePts3D

def rotationMatrix(axis,theta):
    axis = axis/math.sqrt(np.dot(axis,axis))
    a = math.cos(theta/2)
    b, c, d = -axis*math.sin(theta/2)
    return np.array([[a*a+b*b-c*c-d*d, 2*(b*c-a*d), 2*(b*d+a*c)],
                     [2*(b*c+a*d), a*a+c*c-b*b-d*d, 2*(c*d-a*b)],
                     [2*(b*d-a*c), 2*(c*d+a*b), a*a+d*d-b*b-c*c]])

def readSWC(swcFName):
    """
    Read the data of all points in the swc file.
    :return:
    """

    swcPointData = []
    with open(swcFName, 'r') as fle:
        line = fle.readline()
        while not line == '':

            if not line[0] == '#':
                entries = line.split(' ')
                swcPointData.append([float(x) for x in entries[2:7]])

            line = fle.readline()
    return swcPointData

def getAverage(pts, origin = [0, 0, 0], normalize=True):

    av = np.mean(np.asarray(pts) -  np.asarray(origin), axis=0)

    if normalize:
        return av / np.linalg.norm(av)


swcFile = fileopenbox(msg='SWC file with three point soma', filetypes=['*.swc'])
pts = readSWC(swcFile)
ptsAverage = getAverage([x[:3] for x in pts])
print(ptsAverage)