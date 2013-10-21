from GJMorphSim.sim import *

testMorphFile = 'swcFiles/HB060602_3ptSoma.swc'

testSim = BasicSim(morphFile=testMorphFile)
testSim.setSimProps(dt=0.025, tstop=200)
rootStim = testSim.placeRootIClamp(amp=0.05, dur=100, delay=50)
tipVRecs = testSim.recordAllTipsVoltages()
testSim.initAndRun(-65)
tVec = testSim.getTimeVec()
fig1 = tipVRecs[0].plotSeparately(tVec)
tipVRecs[10].addPlotToFig(tVec, fig1, 'b')
tipVRecs[20].addPlotToFig(tVec, fig1, 'g')
tipVRecs[30].addPlotToFig(tVec, fig1, 'm')
tipVRecs[40].addPlotToFig(tVec, fig1, 'c')
tipVRecs[50].addPlotToFig(tVec, fig1, 'k')
showPlot()




