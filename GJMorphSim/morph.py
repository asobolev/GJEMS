import os
import subprocess
import platform
import pkgutil
import math
from GJMorphSim.morphImport import MorphImport, SubTreeWriter
# import matplotlib.pyplot as plt
import numpy as npy

#TODO: LMFilter class to support Specificity feature of L-measure


class LMIO:

    (bit, linkage) = platform.architecture()
    LMPath = 'Lm' + bit[:2] + '/'

    functionRef = ['Soma_Surface',
                   'N_stems',
                   'N_bifs',
                   'N_branch',
                   'N_tips',
                   'Width',
                   'Height',
                   'Depth',
                   'Type',
                   'Diameter',
                   'Diameter_pow',
                   'Length',
                   'Surface',
                   'SectionArea',
                   'Volume',
                   'EucDistance',
                   'PathDistance',
                   'Branch_Order',
                   'Terminal_degree',
                   'TerminalSegment',
                   'Taper_1',
                   'Taper_2',
                   'Branch_pathlength',
                   'Contraction',
                   'Fragmentation',
                   'Daughter_Ratio',
                   'Parent_Daughter_Ratio',
                   'Partition_asymmetry',
                   'Rall_Power',
                   'Pk',
                   'Pk_classic',
                   'Pk_2',
                   'Bif_ampl_local',
                   'Bif_ampl_remote',
                   'Bif_tilt_local',
                   'Bif_tilt_remote',
                   'Bif_torque_local',
                   'Bif_torque_remote',
                   'Last_parent_diam',
                   'Diam_threshold',
                   'HillmanThreshold',
                   'Hausdorff',
                   'Helix',
                   'Fractal_Dim']

    LMOutput = dict(rawData=[],
                    measure1BinCentres=[],
                    measure1BinCounts=[],
                    measure2BinAverages=[],
                    measure2BinStdDevs=[],
                    minimum=None,
                    maximum=None,
                    average=None,
                    CompartmentsConsidered=None,
                    CompartmentsDiscarded=None,
                    TotalSum=None,
                    StdDev=None)
    outputFormat = None

    line1 = ""
    line2 = ""
    line3 = ""

    LMInputFName = 'tmp/LMInput.txt'
    LMOutputFName = 'tmp/LMOutput.txt'
    LMLogFName = 'tmp/LMLog.txt'

    rawDataOutputFlag = False

    packagePrefix = pkgutil.get_loader("GJMorphSim").filename + '/'

    #*******************************************************************************************************************

    def resetOutputData(self):

        self.LMOutput['rawData'] = []
        self.LMOutput['measure1BinCentres'] = []
        self.LMOutput['measure1BinCounts'] = []
        self.LMOutput['measure2BinAverages'] = []
        self.LMOutput['measure2BinStdDevs'] = []
        self.LMOutput['minimum'] = None
        self.LMOutput['maximum'] = None
        self.LMOutput['average'] = None
        self.LMOutput['CompartmentsConsidered'] = None
        self.LMOutput['CompartmentsDiscarded'] = None
        self.LMOutput['TotalSum'] = None
        self.LMOutput['StdDev'] = None
        self.LMOutput['outputFormat'] = None

    #*******************************************************************************************************************

    def __init__(self, morphFile):

        self.rawDataOutputFlag = False

        self.resetOutputData()

        self.line1 = ""
        self.line2 = ""
        self.line3 = morphFile

    #*******************************************************************************************************************

    def writeLMIn(self, line1, line2, line3):


        LMIn = open(self.LMInputFName, 'w')

        if self.rawDataOutputFlag:
            line2 += '-R'

        LMIn.write(line1 + '\n' + line2 + '\n' + line3)
        LMIn.close()

    #*******************************************************************************************************************

    def runLM(self):

        self.resetOutputData()
        if os.path.isfile(self.LMOutputFName):
            os.remove(self.LMOutputFName)
        if os.path.isfile(self.LMLogFName):
            os.remove(self.LMLogFName)

        LMLogFle = open(self.LMLogFName, 'w')
        subprocess.call([self.packagePrefix + self.LMPath + 'lmeasure', self.LMInputFName], \
                                   stdout=LMLogFle, stderr=LMLogFle)

        try:
            LMOutputFile = open(self.LMOutputFName, 'r')
        except:
            print('No Output file created by Lmeasure. Check \'tmp/LMLog.txt\'')
            exit(1)



        LMLogFle.close()

    #*******************************************************************************************************************

    def readlineTrap(self, fle):

        tempStr = fle.readline()
        return tempStr.replace('(0)', '0')

    #*******************************************************************************************************************

    def readOutput(self):

        LMOutputFile = open(self.LMOutputFName, 'r')

        if self.rawDataOutputFlag:

            self.LMOutput['rawData'] = []
            prevLine = LMOutputFile.tell()
            tempStr = self.readlineTrap(LMOutputFile)

            while not tempStr.count('\t'):

                prevLine = LMOutputFile.tell()
                self.LMOutput['rawData'].append(float(tempStr))
                tempStr = self.readlineTrap(LMOutputFile)

            LMOutputFile.seek(prevLine)

        if self.outputFormat == 1:

            tempStr = self.readlineTrap(LMOutputFile)
            tempWords = tempStr.split('\t')
            self.LMOutput['TotalSum'] = float(tempWords[2])
            self.LMOutput['CompartmentsConsidered'] = float(tempWords[3])
            self.LMOutput['CompartmentsDiscarded'] = float(tempWords[4])
            self.LMOutput['Minimum'] = float(tempWords[5])
            self.LMOutput['average'] = float(tempWords[6])
            self.LMOutput['Maximum'] = float(tempWords[7])
            self.LMOutput['StdDev'] = float(tempWords[8])

        elif self.outputFormat == 2:

            tempStr = self.readlineTrap(LMOutputFile)
            tempWords = tempStr.split('\t')
            tempWords = tempWords[2:len(tempWords) - 1]
            self.LMOutput['measure1BinCentres'] = [float(x) for x in tempWords]

            tempStr = self.readlineTrap(LMOutputFile)
            tempWords = tempStr.split('\t')
            tempWords = tempWords[2:len(tempWords) - 1]
            self.LMOutput['measure1BinCounts'] = [float(x) for x in tempWords]

        elif self.outputFormat == 3:

            tempStr = self.readlineTrap(LMOutputFile)
            tempWords = tempStr.split('\t')
            tempWords = tempWords[2:len(tempWords) - 1]
            self.LMOutput['measure1BinCentres'] = [float(x) for x in tempWords]

            tempStr = self.readlineTrap(LMOutputFile)
            tempWords = tempStr.split('\t')
            tempWords = tempWords[2:len(tempWords) - 1]
            self.LMOutput['measure2BinAverages'] = [float(x) for x in tempWords]

            tempStr = self.readlineTrap(LMOutputFile)
            tempWords = tempStr.split('\t')
            tempWords = tempWords[1:len(tempWords) - 1]
            self.LMOutput['measure2BinStdDevs'] = [float(x) for x in tempWords]

        LMOutputFile.close()

    #*******************************************************************************************************************

    def getMeasure(self, measure, Filter=False):

        if not os.path.isdir('tmp'):
            os.mkdir('tmp')

        self.line1 = '-f' + str(self.functionRef.index(measure)) + ',' + '0,0,10'

        self.line2 = '-s' + self.LMOutputFName

        self.writeLMIn(self.line1, self.line2, self.line3)

        self.runLM()

        self.outputFormat = 1
        self.readOutput()

        return self.LMOutput

    #*******************************************************************************************************************

    def getMeasureDistribution(self, measure, nBins=10, Filter=False):

        if not os.path.isdir('tmp'):
            os.mkdir('tmp')

        self.line1 = '-f' + str(self.functionRef.index(measure)) + ','\
                     + 'f' + str(self.functionRef.index(measure)) + ',' + '0,0,' + str(nBins)

        self.line2 = '-s' + self.LMOutputFName

        self.writeLMIn(self.line1, self.line2, self.line3)

        self.runLM()

        self.outputFormat = 2
        self.readOutput()

        return self.LMOutput

    #*******************************************************************************************************************

    #*******************************************************************************************************************

    def getMeasureDependence(self, measure1, measure2, nBins=10, Filter=False):

        if not os.path.isdir('tmp'):
            os.mkdir('tmp')

        self.line1 = '-f' + str(self.functionRef.index(measure1)) + ',' \
                     + 'f' + str(self.functionRef.index(measure2)) + ',' + '1,0,' + str(nBins)

        self.line2 = '-s' + self.LMOutputFName

        self.writeLMIn(self.line1, self.line2, self.line3)

        self.runLM()

        self.outputFormat = 3
        self.readOutput()

        return self.LMOutput

    #*******************************************************************************************************************

#***********************************************************************************************************************


class BasicMorph(MorphImport):

    lmio = None

    #*******************************************************************************************************************

    def __init__(self, morphFile, initDists=False):

        MorphImport.__init__(self, morphFile=morphFile)
        self.lmio = LMIO(morphFile)

        if initDists:
            self.initDistances()

    #*****************************************************************************************************************

    def rect2polar3D1Pt(self, pt):

        r = math.sqrt(pt[0] ** 2 + pt[1] ** 2 + pt[2] ** 2)
        theta = math.acos(pt[2] / r)
        phi = math.atan(pt[1] / pt[0])

        return r, theta, phi

    #*****************************************************************************************************************

    def getTipSperical(self):

        tipSpherical = []
        tempTree = SubTreeWriter(self.rootPtr)

        for secPtr in self.tipPtrs:

            xyzd = tempTree.getSectionxyzd(secPtr)

            tipSpherical.append(self.rect2polar3D1Pt(xyzd[len(xyzd) - 1][:3]))

        return npy.array(tipSpherical)

    #*****************************************************************************************************************

    def getTipUV(self):

        tipUV = []
        tempTree = SubTreeWriter(self.rootPtr)

        for secPtr in self.tipPtrs:

            xyzd = tempTree.getSectionxyzd(secPtr)

            tipUV.append(self.rect2UV1Pt(xyzd[len(xyzd) - 1][:3]))

        return npy.array(tipUV)

    #*****************************************************************************************************************
    def rect2UV1Pt(self, rectCoor):
        '''
        Reference : http://en.wikipedia.org/wiki/UV_mapping
        :param rectCoor:
        :return:
        '''

        unitVector = [x / math.sqrt(npy.dot(rectCoor, rectCoor)) for x in rectCoor]

        u = 0.5 + math.atan2(unitVector[2], unitVector[0]) / 2 / math.pi

        v = 0.5 - math.asin(unitVector[1]) / math.pi\

        return u, v



    #*****************************************************************************************************************