from LMIO.wrapper import *
import matplotlib.pyplot as plt
import os

SWCPath = 'swcFiles/GoodSamplesDLInt1_v2/forager'

swcFNames = ['HB130313-4NS_3ptSoma.swc',
               # 'HB130322-1NS_.swc',
               # 'HB130408-1NS_3ptSoma.swc',
               'HB130425-1NS_3ptSoma.swc',
               # 'HB130501-2NS_STD.swc'
                ]

swcFiles = [os.path.join(SWCPath, x) for x in swcFNames]

# swcFiles.append('swcFiles/HB060602_3ptSoma.swc')

LMOutput = getMeasureDependence(['Bif_ampl_local'], ['Daughter_Ratio'], swcFiles, nBins=1000)


cols = ['r', 'g', 'b', 'm', 'k', 'c']

fig1 = plt.figure()
plt.show(block=False)

for swcInd in range(len(swcFiles)):

    plt.errorbar(LMOutput[0]['measure1BinCentres'][swcInd, :],
             LMOutput[0]['measure2BinAverages'][swcInd, :],
             LMOutput[0]['measure2BinStdDevs'][swcInd, :],
                color=cols[swcInd%6], ls='-', marker='o', ms=5, mfc=cols[swcInd%6])


plt.draw()
