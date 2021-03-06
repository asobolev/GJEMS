from LMIO.wrapper import *
import matplotlib.pyplot as plt
from easygui import fileopenbox
import numpy as np
import sys

# swcFile = fileopenbox(msg='SWC file with three point soma', filetypes=['*.swc'])
assert len(sys.argv) == 2, 'Only one argument, the path of the swcfile expected, ' + str(len(sys.argv)) + 'found'
swcFile = sys.argv[1]
swcFiles = [swcFile]


##*********************************************************************************************************************
## Usage Example getMeasureDistribution
# ##*********************************************************************************************************************
LMOutput = getMeasureDistribution(['Rall_Power'], swcFiles, nBins=100)
plt.figure()

# plt.plot(LMOutput[0]['measure1BinCentres'][0], np.cumsum(LMOutput[0]['measure1BinCounts'][0]), 'ro-', mfc='r', ms=5)
plt.plot(LMOutput[0]['measure1BinCentres'][0], LMOutput[0]['measure1BinCounts'][0], 'ro-', mfc='r', ms=5)
plt.draw()
plt.show(block=False)

##*********************************************************************************************************************

##*********************************************************************************************************************
## # Usage Example getMeasure
##*********************************************************************************************************************
# LMOutput = getMeasure(['EucDistance'], swcFiles)
# # print 'Neuron Surface Area is ' + str(LMOutput[0]['WholeCellMeasures'][0][4])
# print LMOutput[0]['WholeCellMeasures'][0]

##*********************************************************************************************************************

#*********************************************************************************************************************
# Usage Example getMeasureDependence without averaging
#*********************************************************************************************************************
# LMOutput = getMeasureDependence(['N_branch'], ['EucDistance'], swcFiles, nBins=100, average=False)
# plt.figure()
# plt.plot(LMOutput[0]['measure1BinCentres'][0], LMOutput[0]['measure2BinSums'][0], 'ro', mfc='r', ms=5)
# plt.draw()
# plt.show(block=False)

#*********************************************************************************************************************

#*********************************************************************************************************************
# Usage Example getMeasureDependence with averaging
#*********************************************************************************************************************
# LMOutput = getMeasureDependence(['Diameter'], ['EucDistance'], swcFiles, nBins=100, average=True)
# plt.figure()
# plt.errorbar(LMOutput[0]['measure1BinCentres'][0],
#              LMOutput[0]['measure2BinAverages'][0],
#              LMOutput[0]['measure2BinStdDevs'][0],
#                 color='r', ls='-', marker='o', ms=5, mfc='r')
# plt.draw()
# plt.show(block=False)

#*********************************************************************************************************************