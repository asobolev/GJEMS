import sys

sys.path.append('../lib')

from morph import *
import matplotlib.pyplot as plt

testLMIO = LMIO('../swcFiles/HB060602_3ptSoma.swc')

diamHist = testLMIO.getMeasureDistribution('Diameter', nBins=50)
plt.figure()

print diamHist[0]
print diamHist[1]
plt.bar(diamHist[0], diamHist[1])
plt.draw()
plt.show(block=True)