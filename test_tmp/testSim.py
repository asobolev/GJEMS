from easygui import fileopenbox

import matplotlib.pyplot as plt
import numpy as np

from GJEMS.sim.sim import *


testMorphFile = fileopenbox(msg='SWC file with three point soma', filetypes=['*.swc'])

testSim = BasicSim(morphFile=testMorphFile)
testSim.setSimProps(dt=0.1, tstop=70)
rootStim = testSim.placeRootIClamp(amp=0.05, dur=50, delay=10)
nTips = len(testSim.tipPtrs)
toRecord = np.random.random_integers(low=0, high=nTips, size=5)
tipVRecs = []
for ind in toRecord:
    tipVRecs.append(testSim.recordTipVoltage(testSim.tipPtrs[ind]))

testSim.initAndRun(-65)
tVec = testSim.getTimeVec()
fig1 = plt.figure()
plt.show(block=False)

cols = ['r', 'g', 'b', 'm', 'k', 'c']
for tipVRec, col in zip(tipVRecs, cols):
    tipVRec.addPlotToFig(tVec, fig1, col)
plt.draw()




