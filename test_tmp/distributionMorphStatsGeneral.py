from LMIO.wrapper import *
import matplotlib.pyplot as plt
import os
import numpy as np

SWCPath = 'swcFiles/GoodSamplesDLInt1_v2/forager'

swcFNames = ['HB130313-4NS_3ptSoma.swc',
               # 'HB130322-1NS_.swc',
               'HB130408-1NS_3ptSoma.swc',
               'HB130425-1NS_3ptSoma.swc',
               # 'HB130501-2NS_STD.swc'
                ]

swcFiles = [os.path.join(SWCPath, x) for x in swcFNames]

# swcFiles.append('swcFiles/HB060602_3ptSoma.swc')

LMOutput = getMeasureDistribution(['Daughter_Ratio'], swcFiles, nBins=100)


cols = ['r', 'g', 'b', 'm', 'k', 'c']

fig1 = plt.figure()
plt.show(block=False)

for swcInd in range(len(swcFiles)):
    temp = LMOutput[0]['measure1BinCounts'][swcInd, :]
    normMeasure = np.cumsum(temp / sum(temp))
    plt.plot(LMOutput[0]['measure1BinCentres'][swcInd, :], normMeasure,
                color=cols[swcInd%6], marker='o', mfc=cols[ swcInd%6], ms=5)

plt.draw()
