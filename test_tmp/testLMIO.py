from GJMorphSim.morph import *
import matplotlib.pyplot as plt

testLMIO = LMIO('swcFiles/HB060602_3ptSoma.swc')

# #*********************************************************************************************************************
# # Testing LMIO.getMeasureDistribution
# #*********************************************************************************************************************
# LMOutput = testLMIO.getMeasureDistribution('Diameter', nBins=50)
# plt.figure()
#
#
# print LMOutput['measure1BinCentres']
# print LMOutput['measure1BinCounts']
# plt.bar(LMOutput['measure1BinCentres'], LMOutput['measure1BinCounts'])
# plt.draw()
# plt.show(block=True)
#
# #*********************************************************************************************************************

# #*********************************************************************************************************************
# # Testing LMIO.getMeasure
# #*********************************************************************************************************************
# LMOutput = testLMIO.getMeasure('Height')
# print 'Neuron Height is ' + str(LMOutput['average'])
#
# #*********************************************************************************************************************

#*********************************************************************************************************************
# Testing LMIO.getMeasureDependence
#*********************************************************************************************************************
LMOutput = testLMIO.getMeasureDependence('Bif_ampl_local', 'EucDistance', nBins=50)
plt.figure()


plt.bar(LMOutput['measure1BinCentres'], LMOutput['measure2BinAverages'])
plt.draw()
plt.show(block=True)

#***********************************************************************************************************************