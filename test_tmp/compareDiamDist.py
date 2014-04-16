from LMIO.wrapper import *
import matplotlib.pyplot as plt
import numpy as np

swcFiles = ['swcFiles/HB060602_3ptSoma.swc',
            'swcFiles/GoodSamplesDLInt1_v2/HB130408-1NS/012_all_H.swc',
            'swcFiles/GoodSamplesDLInt1_v2/HB130408-1NS/012_all_L.swc',
            '/home/ajay/PowerFolders/GinJangNDB_Upload/SigenSegmentations/Results/GoodSamplesDLInt1_v1/forager/'
            + 'HB130408-1NS_3ptSoma.swc',
           '/home/ajay/PowerFolders/GinJangNDB_Upload/SigenSegmentations/Experimentation/HB130408-1/swc/'
           + 'D00V00C00S00_3ptSoma.swc']
LMOutput = getMeasureDistribution(['Diameter'], swcFiles, nBins=50)

cols = ['r', 'g', 'b', 'm', 'k', 'c']

plt.figure()
plt.show(block=False)

for swcInd in range(len(swcFiles)):

    totalSections = sum(LMOutput[0]['measure1BinCounts'][swcInd, :])
    plt.plot(LMOutput[0]['measure1BinCentres'][swcInd, :],
            100 * LMOutput[0]['measure1BinCounts'][swcInd, :] / totalSections,
            color=cols[swcInd], marker='*', ms=5)

plt.legend(['HB060602', 'HB130408-1v2_H', 'HB130408-1v2_L', 'HB130408-1v1', 'HB130408-1Bad'])
plt.suptitle('Comparing Diameter Distribution (v1:Feb 2014, v2:Apr 2014, L:1um, H:0.5um)')
plt.xlabel('Diameter(micrometer)')
plt.ylabel('Percentage of Sections')
plt.draw()