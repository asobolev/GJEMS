import matplotlib.pyplot as plt
from GJEMS.morph.morph import plotPoints3D, addPoints3D
import json
import subprocess
import numpy as np
import os
from mpl_toolkits.mplot3d import Axes3D

def getTipXYZ(swcFile):
    output = subprocess.check_output(['python', 'getTipXYZ.py', swcFile])
    startStr = 'startJSON'
    return json.loads(output[output.find(startStr) + len(startStr): -1])

def getSubtreeName(swcFile, label):

    swcFilePath, swcFName = os.path.split(swcFile)
    swcFNameRoot = swcFName[:-4]
    return os.path.join(swcFilePath, swcFNameRoot + '_subTrees', swcFNameRoot + label + '.swc')

def getSubtreeDirName(swcFile):

    swcFilePath, swcFName = os.path.split(swcFile)
    swcFNameRoot = swcFName[:-4]
    return os.path.join(swcFilePath, swcFNameRoot + '_subTrees')

swcFiles = [
    # 'swcFiles/GoodSamplesDLInt1_v2/forager/HB130425-1NS_3ptSoma_FSTD.swc',
    'swcFiles/GoodSamplesDLInt1_v2/forager/HB130313-4NS_3ptSoma_FSTD.swc',
    # 'swcFiles/GoodSamplesDLInt1_v2/forager/HB130408-1NS_3ptSoma_FSTD.swc',
    'swcFiles/GoodSamplesDLInt1_v2/forager/HB130501-2NS_3ptSoma_FSTD.swc',
    'swcFiles/GoodSamplesDLInt1_v2/forager/HB130322-1NS_3ptSoma_FSTD.swc',
    # 'swcFiles/HB060602_3ptSoma_STD.swc'
]
cols = ['r', 'g', 'b', 'm', 'k', 'c']

labels = ['_db', '_vb']


fig1 = plt.figure()
plt.show(block=False)



for swcFile, col in zip(swcFiles, cols):

    if not os.path.isdir(getSubtreeDirName(swcFile)):
        print('Subtree directory not found. Creating subtrees')
        subprocess.call(['python', 'writeSubTrees.py', swcFile])

    for labelInd, label in enumerate(labels):

        tipXYZ = np.asarray(getTipXYZ(getSubtreeName(swcFile, label)))
        plt.figure(fig1.number)
        plt.subplot(len(labels), 1, labelInd + 1)
        # print min(tipXYZ[:, 2]), max(tipXYZ[:, 2])
        minZ = -100
        maxZ = 100
        targetMeanDist = 250
        meanDist = np.mean([np.linalg.norm(x) for x in tipXYZ])
        scalingFactor = targetMeanDist / meanDist
        for XYZ in tipXYZ:

            # col = 'b'
            XYZ *= scalingFactor
            col = plt.cm.jet((XYZ[2] - minZ) / (maxZ - minZ))
            plt.plot(XYZ[0], XYZ[1], color=col, marker='o', mfc=col, ms=5)
        plt.title(label)
        plt.xlabel('x')
        plt.ylabel('y')

    plt.subplot(211)
    plt.ylim([-300, 200])
    plt.xlim([-100, 400])

    plt.subplot(212)
    plt.ylim([-500, 200])
    plt.xlim([-100, 400])

    plt.draw()
    # plt.savefig(os.path.split(swcFile)[-1][:-4] + '.png')
    # plt.subplot(211)
    # plt.cla()
    # plt.subplot(212)
    # plt.cla()

    # tipXYZ = np.asarray(getTipXYZ(swcFile))
    #
    #
    # # print min(tipXYZ[:, 2]), max(tipXYZ[:, 2])
    # minZ = -100
    # maxZ = 100
    # targetMeanDist = 250
    # meanDist = np.mean([np.linalg.norm(x) for x in tipXYZ])
    # scalingFactor = targetMeanDist / meanDist
    # for XYZ in tipXYZ:
    #
    #     # col = 'b'
    #     XYZ *= scalingFactor
    #     col = plt.cm.jet((XYZ[2] - minZ) / (maxZ - minZ))
    #     plt.plot([XYZ[0]], [XYZ[1]], [XYZ[2]],color=col, marker='o', mfc=col, ms=3)
    #
    # plt.xlabel('x')
    # plt.ylabel('y')


plt.draw()