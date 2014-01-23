from GJEMS.morph import *
from LMIO.wrapper import *
from neuronvisio.controls import Controls
from easygui import fileopenbox
import os
import shutil
import time
import json


swcfName = fileopenbox(msg='SWC file with three point soma', filetypes=['*.swc'])
testMorph = BasicMorph(swcfName)

#***********************************************************************************************************************
controls = Controls()
time.sleep(5)
controls.launch_visio()
time.sleep(5)
dirName = swcfName.strip('.swc') + '_images'

if os.path.isdir(dirName):
    shutil.rmtree(dirName)

os.mkdir(dirName)

scene = controls.visio.mayavi.visualization.scene
mlab = scene.mlab
scene.camera.zoom(1.3)

for azimuthAngleInd in range(8):
    mlab.savefig(os.path.join(dirName,'azimuth' + str(azimuthAngleInd * 45) + '.png'), size=[1600, 1200])
    scene.camera.azimuth(45)


presElevation = 0
for elevationAngleInd in range(4):
    mlab.savefig(os.path.join(dirName,'elevation' + str(presElevation) + '.png'), size=[1600, 1200])
    scene.camera.elevation(-22.5)
    presElevation -= 22.5

scene.camera.elevation(90)
presElevation += 90


# for elevationAngleInd in range(3):
#     scene.camera.elevation(22.5)
#     presElevation += 22.5
#     mlab.savefig(os.path.join(dirName,'elevation' + str(presElevation) + '.png'), size=[1600, 1200])

#***********************************************************************************************************************

print 'Calculating PCA details'
evecs, stds = getPCADetails(swcfName)

#***********************************************************************************************************************

print 'Calculating Simple Morphometrics'

measureNames = ['Width', 'Height', 'Depth', 'Length', 'Volume', 'Surface', 'N_bifs']

LMOutputSimple = getMeasure(measureNames, [swcfName])
width = LMOutputSimple[0]['WholeCellMeasures'][0][0]
height = LMOutputSimple[1]['WholeCellMeasures'][0][0]
depth = LMOutputSimple[2]['WholeCellMeasures'][0][0]
length = LMOutputSimple[3]['WholeCellMeasures'][0][0]
volume = LMOutputSimple[4]['WholeCellMeasures'][0][0]
surface = LMOutputSimple[5]['WholeCellMeasures'][0][0]
nbifs = LMOutputSimple[6]['WholeCellMeasures'][0][0]

print 'Calculating Scholl Morphometrics'

LMOutputScholl = getMeasureDependence(['N_branch'], ['EucDistance'], [swcfName], nBins=100, average=False)

distanceBins = LMOutputScholl[0]['measure1BinCentres'][0]
noOfIntersections = LMOutputScholl[0]['measure2BinSums'][0]

jsonDict = dict(
                width=width,
                height=height,
                depth=depth,
                length=length,
                volume=volume,
                surface=surface,
                nbifs=nbifs,
                evecs=evecs.tolist(),
                stds=stds.tolist(),
                shollBins=distanceBins.tolist(),
                shollCounts=noOfIntersections.tolist()
                )

jsonStr = json.dumps(jsonDict)
#***********************************************************************************************************************