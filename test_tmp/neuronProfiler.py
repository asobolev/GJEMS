#Author: Ajayrama Kumaraswamy(ajayramak@bio.lmu.de)
#Date: 3 March 2014
#Place: Dept. of Biology II, LMU, Munich


#********************************************List of Dependencies*******************************************************
#The following code has been tested with the indicated versions on 64bit Linux and PYTHON 2.7.3
#
#LMIO: available at https://github.com/ajayramak/python-Lmeasure.git, with version as of March 2014(Sorry for
#																						not versioning properly)
#os: Use standard library with comes with python.
#subprocess: Use standard library with comes with python.
#shutil : Use standard library with comes with python.
#json : 2.0.9
#sys: Use standard library with comes with python.
#numpy: 1.6.1
#blender: 2.6.9
#IMPORTANT: This file can only be used in conjuction with 'blenderCodeTemplate.py'
#******************************************************Usage************************************************************

#call this script with the path(full/relative) of an swc file as an command-line arguement.

#E.g.: python neuronProfiler.py /home/....../neuron.swc

#Creates a folder in the path of the swc file(neuron_morphData in the above example) and creates two files within it:
#(i)morphometrics.json which contains some morphometric parameters of swc file and
#(ii)neuron.obj file which contains the 3D reconstruction of the swc file(can be opened with softwares like
#blender, mayavi, g3dviewer, etc).
#***********************************************************************************************************************

from LMIO.wrapper import *
import os
import subprocess
import shutil
import json
import sys
import numpy as np


#***********************************************************************************************************************

def getPCADetails(swcFileName):
    """
    Returns the PCA directions and the standard deviations along the principal axes for the set of points(each as a 3D Vector) in the swc file.
    PCA is applied after centering the data about their mean.
    :param swcFileName: Absolute path of the swcfile
    :return:evecs, stds
    evec: 3x3 numpy array, each row is a principal direction, in order of significance.
    stds: Numpy array of shape (3,) with each entry corresponding to the standard deviation along each of the principal directions above about the mean of the data.
    """

    data = np.loadtxt(swcFileName)[:, 2:5]
    mu = np.mean(data, axis=0)
    data = data - mu
    evec, eval,v = np.linalg.svd(data.T, full_matrices=False)
    dataProj = np.dot(data, evec)
    newStds = np.std(dataProj, axis=0)
    return evec, newStds

#***********************************************************************************************************************


assert len(sys.argv) == 2, 'Only one argument, the path of the swcfile expected, ' + str(len(sys.argv)) + 'found'
swcfName = sys.argv[1]
swcDir = os.path.split(swcfName)[0]


with open(swcfName.rstrip('.swc') + '.log', 'w') as morphLogFile:

    #*******************************************************************************************************************
    #This part checks if the output directroy and an OBJ file already exist. Then only the JSON file is replaced, retaining the OBJ file.

    dirName = swcfName.rstrip('.swc') + '_morphData'
    objExists = False

    if os.path.isdir(dirName):

        if 'neuron.obj' in os.listdir(dirName):
            objExists = True
            shutil.move(os.path.join(dirName,'neuron.obj'), os.path.join(swcDir, 'neuron.obj'))

        shutil.rmtree(dirName)

    os.mkdir(dirName)

    if objExists:
        shutil.move(os.path.join(swcDir, 'neuron.obj'), os.path.join(dirName,'neuron.obj'))

    #*******************************************************************************************************************
    #Copy the blender template file, append the necessary lines, and run it to generate the OBJ file, if necessary.

    if not objExists:
        shutil.copy('blenderCodeTemplate.py','blenderCode.py')

        with open('blenderCode.py','a') as blenderCodeFile:

            blenderCodeFile.write('blenderSWC = BlenderSWCImporter(\'' + swcfName + '\')\n')
            blenderCodeFile.write('blenderSWC.export2Obj(\'' + os.path.join(dirName,'neuron.obj') + '\')')

        subprocess.call(['blender', '--background', '--python', 'blenderCode.py'], stdout=morphLogFile, stderr=morphLogFile)
        os.remove('blenderCode.py')

    #*******************************************************************************************************************

    #Calculate PCA stats
    morphLogFile.write('Calculating PCA details')
    evecs, stds = getPCADetails(swcfName)

    #*******************************************************************************************************************
    #Calculate the other morphometeric stats using python-Lmeasure, format everything in a JSON str and write.

    morphLogFile.write('Calculating Simple Morphometrics')

    measureNames = ['Width', 'Height', 'Depth', 'Length', 'Volume', 'Surface', 'N_bifs']

    LMOutputSimple = getMeasure(measureNames, [swcfName])
    width = LMOutputSimple[0]['WholeCellMeasures'][0][0]
    height = LMOutputSimple[1]['WholeCellMeasures'][0][0]
    depth = LMOutputSimple[2]['WholeCellMeasures'][0][0]
    length = LMOutputSimple[3]['WholeCellMeasures'][0][0]
    volume = LMOutputSimple[4]['WholeCellMeasures'][0][0]
    surface = LMOutputSimple[5]['WholeCellMeasures'][0][0]
    nbifs = LMOutputSimple[6]['WholeCellMeasures'][0][0]

    morphLogFile.write('Calculating Scholl Morphometrics')

    LMOutputScholl = getMeasureDependence(['N_branch'], ['EucDistance'], [swcfName], nBins=100, average=False)

    distanceBins = LMOutputScholl[0]['measure1BinCentres'][0]
    noOfIntersections = LMOutputScholl[0]['measure2BinSums'][0]

    scalarDict = dict(
                    width=width,
                    height=height,
                    depth=depth,
                    length=length,
                    volume=volume,
                    surface=surface,
                    nbifs=nbifs,
                    )

    vectorDict = dict(
                    pcaDirs=evecs.tolist(),
                    pcaStds=stds.tolist(),
                    shollBins=distanceBins.tolist(),
                    shollCounts=noOfIntersections.tolist()
                    )

    jsonDict = dict(vectorMeasurements=vectorDict, scalarMeasurements=scalarDict)

    with open(os.path.join(dirName,'morphometrics.json'), 'w') as fle:
        jsonStr = json.dump(jsonDict, fle)
    #*******************************************************************************************************************