import matplotlib.pyplot as plt
import json
import subprocess
import numpy as np
import os

def getTipUV(swcFile):
    output = subprocess.check_output(['python', 'getTipUV.py', swcFile])
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
            # 'swcFiles/GoodSamplesDLInt1_v2/newlyEmerged/HB130523-3NS_3ptSoma_FSTD.swc',
            'swcFiles/GoodSamplesDLInt1_v2/newlyEmerged/HB130605-1NS_3ptSoma_FSTD.swc',
            # 'swcFiles/GoodSamplesDLInt1_v2/newlyEmerged/HB130605-2NS_3ptSoma_FSTD.swc'
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


        rtrned = getTipUV(getSubtreeName(swcFile, label))
        uvPts = np.asarray(rtrned[0])
        actualRadii = np.asarray(rtrned[1])
        meanRadius = np.mean(actualRadii)
        stdRadius = np.std(actualRadii)
        minRadiusForPlot = meanRadius - 2 * stdRadius
        colsToUse = plt.cm.jet((actualRadii - minRadiusForPlot) / (4 * stdRadius))


        plt.figure(fig1.number)
        plt.subplot(len(labels), 1, labelInd + 1)
        for uvPt, col2Use in zip(uvPts, colsToUse):
            plt.plot(uvPt[0], uvPt[1], marker='o', ls='None', color=col2Use, mfc=col2Use, ms=3.5)
        plt.title(label)
        plt.xlim([0.25, 0.75])
        plt.ylim([0, 1])

plt.draw()



