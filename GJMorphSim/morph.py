import os
#TODO: use subprocess package
import platform
import pkgutil
import os
from GJMorphSim.morphImport import MorphImport
# import matplotlib.pyplot as plt
# import numpy as npy

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

    rawData = []
    measure1BinCentres = []
    measure1BinCounts = []
    measure2BinAverages = []
    measure2BinStdDevs = []
    minimum = None
    maximum = None
    average = None
    CompartmentsConsidered = None
    CompartmentsDiscarded = None
    TotalSum = None
    StdDev = None
    outputFormat = None

    line1 = ""
    line2 = ""
    line3 = ""

    LMInputFName = 'tmp/LMInput.txt'
    LMOutputFName = 'tmp/LMOutput.txt'

    rawDataOutputFlag = False

    packagePrefix = pkgutil.get_loader("GJMorphSim").filename + '/'

    #*******************************************************************************************************************

    def resetOutputData(self):

        self.rawData = []
        self.measure1BinCentres = []
        self.measure1BinCounts = []
        self.measure2BinAverages = []
        self.measure2BinStdDevs = []
        self.minimum = None
        self.maximum = None
        self.average = None
        self.CompartmentsConsidered = None
        self.CompartmentsDiscarded = None
        self.TotalSum = None
        self.StdDev = None
        self.outputFormat = None

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
        LMIn.write(line1 + '\n' + line2 + '\n' + line3)
        LMIn.close()

    #*******************************************************************************************************************

    def runLM(self, LMInputFName):

        dump = os.system(self.packagePrefix + self.LMPath + 'lmeasure ' + LMInputFName)

    #*******************************************************************************************************************

    def readOutput(self, LMOutputFName):

        LMOutputFile = open(LMOutputFName, 'r')

        if self.rawDataOutputFlag:

            #TODO
            pass

        if self.outputFormat == 1:

            #TODO
            pass

        elif self.outputFormat == 2:

            tempStr = LMOutputFile.readline()
            tempWords = tempStr.split('\t')
            tempWords = tempWords[2:len(tempWords) - 1]
            self.measure1BinCentres = [float(x) for x in tempWords]

            tempStr = LMOutputFile.readline()
            tempWords = tempStr.split('\t')
            tempWords = tempWords[2:len(tempWords) - 1]
            self.measure1BinCounts = [float(x) for x in tempWords]

        elif self.outputFormat == 3:

            #TODO
            pass

        elif self.outputFormat == 4:

            #TODO
            pass

        LMOutputFile.close()

    #*******************************************************************************************************************

    def getMeasureDistribution(self, measure, average=False, nBins=10, Filter=False):

        if not os.path.isdir('tmp'):
            os.mkdir('tmp')

        self.line1 = '-f' + str(self.functionRef.index(measure)) + ','\
                     + 'f' + str(self.functionRef.index(measure)) + ',' + str(int(average)) + ',0,' + str(nBins)

        self.line2 = '-s' + self.LMOutputFName

        self.writeLMIn(self.line1, self.line2, self.line3)

        self.runLM(self.LMInputFName)

        self.outputFormat = 2
        self.readOutput(self.LMOutputFName)

        return [self.measure1BinCentres, self.measure1BinCounts]

    #*******************************************************************************************************************


#***********************************************************************************************************************


class BasicMorph(MorphImport):

    swcFileName = None

    #*******************************************************************************************************************

    def __init__(self, morphFile):

        MorphImport.__init__(self, morphFile=morphFile)

        self.swcFileName = morphFile

    #*******************************************************************************************************************