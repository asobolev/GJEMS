import sys

sys.path.append('../lib')

from morph import *

testLMIO = LMIO('../swcFiles/HB060602_3ptSoma.swc')

diamHist = testLMIO.getMeasureDistribution('Diameter')

print diamHist