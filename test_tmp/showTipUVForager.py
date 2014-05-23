import matplotlib.pyplot as plt
from GJEMS.morph.morph import plotPoints3D, addPoints3D
import json
import subprocess
import numpy as np
import os
from mpl_toolkits.mplot3d import Axes3D

def getTipUV(swcFile, suffix):
    output = subprocess.check_output(['python', 'getTipUV' + suffix + '.py', swcFile])
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


        rtrned = getTipUV(getSubtreeName(swcFile, label), 'OpenX')
        uvPts = np.asarray(rtrned[0])
        actualRadii = np.asarray(rtrned[1])
        meanRadius = np.mean(actualRadii)
        stdRadius = np.std(actualRadii)
        minRadiusForPlot = meanRadius - 2 * stdRadius
        # colsToUse = plt.cm.jet((actualRadii - minRadiusForPlot) / (4 * stdRadius))
        colsToUse = [col] * len(actualRadii)

        plt.figure(fig1.number)
        plt.subplot(len(labels), 2, 2 * labelInd + 1)

        for uvPt, col2Use in zip(uvPts, colsToUse):
            plt.plot(uvPt[0], uvPt[1], marker='o', ls='None', color=col2Use, mfc=col2Use, ms=5)

        plt.title(label)
        plt.xlim([0.25, 0.75])
        plt.ylim([0, 1])
        plt.xlabel('z')
        plt.ylabel('-y')


        rtrned = getTipUV(getSubtreeName(swcFile, label), 'OpenY')
        uvPts = np.asarray(rtrned[0])
        actualRadii = np.asarray(rtrned[1])
        meanRadius = np.mean(actualRadii)
        stdRadius = np.std(actualRadii)
        minRadiusForPlot = meanRadius - 2 * stdRadius
        # colsToUse = plt.cm.jet((actualRadii - minRadiusForPlot) / (4 * stdRadius))
        colsToUse = [col] * len(actualRadii)

        plt.figure(fig1.number)
        plt.subplot(len(labels), 2, 2 * labelInd + 2)

        for uvPt, col2Use in zip(uvPts, colsToUse):
            plt.plot(uvPt[0], uvPt[1], marker='o', ls='None', color=col2Use, mfc=col2Use, ms=5)

        plt.title(label)
        # plt.xlim([0.25, 0.75])
        plt.xlim([0, 1])
        plt.ylim([0, 1])
        plt.xlabel('z')
        plt.ylabel('-x')

    # rtrned = getTipUV(swcFile, 'OpenX')
    # uvPts = np.asarray(rtrned[0])
    # actualRadii = np.asarray(rtrned[1])
    # meanRadius = np.mean(actualRadii)
    # stdRadius = np.std(actualRadii)
    # minRadiusForPlot = meanRadius - 2 * stdRadius
    # colsToUse = plt.cm.jet((actualRadii - minRadiusForPlot) / (4 * stdRadius))
    # # colsToUse = [col] * len(actualRadii)
    #
    #
    # plt.figure(fig1.number)
    # plt.subplot(2, 1, 1)
    #
    # for uvPt, col2Use, actualRadius in zip(uvPts, colsToUse, actualRadii):
    #     plt.plot([uvPt[0]], [uvPt[1]], marker='o', ls='None', color=col2Use, mfc=col2Use, ms=5)
    #
    # plt.xlim([0.25, 0.75])
    # plt.ylim([0, 1])
    # plt.xlabel('z')
    # plt.ylabel('-y')
    #
    #
    # rtrned = getTipUV(swcFile, 'OpenY')
    # uvPts = np.asarray(rtrned[0])
    # actualRadii = np.asarray(rtrned[1])
    # meanRadius = np.mean(actualRadii)
    # stdRadius = np.std(actualRadii)
    # minRadiusForPlot = meanRadius - 2 * stdRadius
    # colsToUse = plt.cm.jet((actualRadii - minRadiusForPlot) / (4 * stdRadius))
    # # colsToUse = [col] * len(actualRadii)
    #
    # plt.figure(fig1.number)
    # plt.subplot(2, 1, 2)
    #
    # for uvPt, col2Use, actualRadius in zip(uvPts, colsToUse, actualRadii):
    #     plt.plot([uvPt[0]], [uvPt[1]], marker='o', ls='None', color=col2Use, mfc=col2Use, ms=5)
    #
    # plt.xlim([0, 1])
    # plt.ylim([0, 0.5])
    # plt.xlabel('z')
    # plt.ylabel('-x')


plt.draw()
