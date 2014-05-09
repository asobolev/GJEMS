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


swcFiles = ['swcFiles/GoodSamplesDLInt1_v2/forager/HB130425-1NS_3ptSoma_STD.swc',
            'swcFiles/GoodSamplesDLInt1_v2/forager/HB130313-4NS_3ptSoma_STD.swc',
            'swcFiles/GoodSamplesDLInt1_v2/forager/HB130408-1NS_3ptSoma_STD.swc',
            'swcFiles/GoodSamplesDLInt1_v2/forager/HB130501-2NS_3ptSoma_STD.swc',
            'swcFiles/GoodSamplesDLInt1_v2/forager/HB130322-1NS_3ptSoma_STD.swc',
            # 'swcFiles/HB060602_3ptSoma_STD.swc'
            ]
cols = ['r', 'g', 'b', 'm', 'k', 'c']

labels = ['_db', '_vb']


fig1 = plt.figure()
plt.show(block=False)

for swcFile, col in zip(swcFiles, cols):

    for labelInd, label in enumerate(labels):

        plt.subplot(len(labels), 1, labelInd + 1)
        uvPts = np.asarray(getTipUV(getSubtreeName(swcFile, label)))
        plt.plot(uvPts[:, 0], uvPts[:, 1], marker='*', ls='None', color=col, mfc=col)
        plt.title(label)

plt.draw()
