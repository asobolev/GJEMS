from GJMorphSim.morph import *


import matplotlib.pyplot as pyplot

testMorphFile = 'swcFiles/HB060602_3ptSoma_subTrees/HB060602_3ptSoma_db.swc'

testMorph = BasicMorph(morphFile=testMorphFile)

sfig = pyplot.figure()

spher = testMorph.getTipSperical()
pyplot.plot(spher[:, 1], spher[:, 2], 'ro', mfc='r', ms=5)

uvfig = pyplot.figure()

uv = testMorph.getTipUV()
pyplot.plot(uv[:, 0], uv[:, 1], 'ro', mfc='r', ms=5)

pyplot.show(block=True)
