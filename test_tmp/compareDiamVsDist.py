import numpy as np
from LMIO.wrapper import *
import matplotlib.pyplot as plt




def addDepPlot(fig, Bin, Count, Stds, colour):

    plt.figure(fig.number)
    plt.errorbar(Bin, Count, Stds, color=colour, ls='None', marker='o', ms=5, mfc=colour)
    plt.draw()


def drawDeps(fig, Bins, Counts, Stds, cols):

    for bins, counts, stds, col in zip(Bins, Counts, Stds, cols):
        addDepPlot(fig, bins, counts, stds, col)

fig = plt.figure()
plt.show(block=False)

swcFiles = ['swcFiles/HB060602_3ptSoma.swc',
            'swcFiles/GoodSamplesDLInt1_v2/HB130408-1NS/012_all_H.swc',
            'swcFiles/GoodSamplesDLInt1_v2/HB130408-1NS/012_all_L.swc',
            '/home/ajay/PowerFolders/GinJangNDB_Upload/SigenSegmentations/Results/GoodSamplesDLInt1_v1/forager/'
            + 'HB130408-1NS_3ptSoma.swc']

LMOutput = getMeasureDependence(['Diameter'], ['EucDistance'], swcFiles, nBins=50, average=True)


drawDeps(fig, LMOutput[0]['measure1BinCentres'], LMOutput[0]['measure2BinAverages'], LMOutput[0]['measure2BinStdDevs'],
            ['r', 'g', 'b', 'm'])
plt.figure(fig.number)
plt.legend(['HB060602', 'HB130408-1v2_H', 'HB130408-1v2_L', 'HB130408-1v1'])
plt.suptitle('Comparing Diameter Vs Distance plots (v1:Feb 2014, v2:Apr 2014, L:1um, H:0.5um)')
plt.xlabel('Distance from Root(micrometer)')
plt.ylabel('Diameter(micrometer)')
plt.draw()