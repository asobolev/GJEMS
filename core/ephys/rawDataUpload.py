import os
from neo import Spike2IO, Segment, Block
import quantities as qu
import gnodeclient
from .GNodeUpoadHelpers import *
import odml
import csv

#*******************************************************************************************************************


def extractCSVMetaData(csvFile, blockName):

    csvData = dict(freqs=[], pulse=[[], []], spont=False, resp='')
    csvFle = open(csvFile, 'rb')

    csvReader = csv.reader(csvFle, dialect='excel')

    thash = csvReader.next()

    lne = csvReader.next()

    freqCol = lne.index('Frequency')
    pulseCol = lne.index('Pulse')
    spontCol = lne.index('Spontaneous')
    respCol = lne.index('Response')

    targetID = blockName

    presID = ''

    try:
        while not presID == targetID:

            lne = csvReader.next()
            presID = lne[0]
    except StopIteration:
        raise IOError('CSV file supplied does not have information of the given SMR file.')

    csvData['freqs'] = [float(x) * qu.Hz for x in lne[freqCol].split(',')]
    unresolved = []
    try:
        for word in lne[pulseCol].split(','):
            if word.count('/'):
                (duration, interval) = word.split('/')
                unresolved.append(float(duration) * qu.ms)
                csvData['pulse'][1].extend([float(interval) * qu.ms] * len(unresolved))
                csvData['pulse'][0].extend(unresolved)
                unresolved = []
            else:
                unresolved.append(float(word) * qu.ms)

        csvData['pulse'][1].extend(unresolved)
        lastNum = csvData['pulse'][0][len(csvData['pulse'][0]) - 1]
        csvData['pulse'][0].extend([lastNum] * len(unresolved))
    except:
        raise(Exception('Improper entry in pulse column for the given smr file.'))

    spontStr = lne[spontCol]
    csvData['spont'] = bool(spontStr.count('yes') + spontStr.count('Yes') + spontStr.count('YES'))
    csvData['resp'] = lne[respCol]

    csvFle.close()
    return  csvData

#***********************************************************************************************************************


class RawDataUploader():

    dataBlock = None
    dataBlockToUpload = None
    spike2Reader = None
    voltageSignal = None
    vibrationSignal = None
    GNodeSession = None
    csvData = None
    blockName = None
    mainSec = None
    expName = None

    #*******************************************************************************************************************

    def __init__(self, ephysFile, csvFile):

        assert os.path.isfile(ephysFile), 'SMR file not found'
        assert os.path.isfile(csvFile), 'csv file not found'

        self.ephysFile = ephysFile
        self.expName = os.path.split(ephysFile)[1].strip('.smr')
        self.blockName = self.expName + '_raw'
        self.csvFile = csvFile
        self.GNodeSession = gnodeclient.session.create(location="http://predata.g-node.org",
                                                       username="bob", password="pass")

    #*******************************************************************************************************************

    def checkExistenceOnServer(self):

        return checkIfExistsSection(self.GNodeSession, self.expName)

    #*******************************************************************************************************************

    def deleteExistent(self):

        deleteExistentBlock(self.GNodeSession, self.blockName)
        deleteExistentSection(self.GNodeSession, self.expName)

    #*******************************************************************************************************************

    def parseSpike2Data(self):

        spike2Reader = Spike2IO(self.ephysFile)
        self.dataBlock = spike2Reader.read()[0]

        entireVoltageSignal = self.dataBlock.segments[0].analogsignals[0]
        entireVibrationSignal = self.dataBlock.segments[0].analogsignals[1]

        recordingStartTime = max(entireVibrationSignal.t_start, entireVoltageSignal.t_start)
        recordingEndTime = min(entireVibrationSignal.t_stop, entireVoltageSignal.t_stop)

        for eventArray in self.dataBlock.segments[0].eventarrays:
            if len(eventArray.times) == 2:
                recordingStartTime = eventArray.times[0]
                recordingEndTime = eventArray.times[1]

        recordingStartIndex = int((recordingStartTime - entireVoltageSignal.t_start)
                                  * entireVoltageSignal.sampling_rate)
        recordingEndIndex = int((recordingEndTime - entireVoltageSignal.t_start) * entireVoltageSignal.sampling_rate)

        self.vibrationSignal = entireVibrationSignal[recordingStartIndex:recordingEndIndex + 1] * 27.2 * qu.um
        self.voltageSignal = entireVoltageSignal[recordingStartIndex:recordingEndIndex + 1] * 20 * qu.mV

    #*******************************************************************************************************************

    def uploadToGNode(self):

        self.csvData = extractCSVMetaData(self.csvFile, self.expName)

        self.dataBlockToUpload = Block(name=self.blockName, file_origin=self.expName)

        raw_seg = Segment(name='rawData', index=0)

        self.vibrationSignal.name = 'Vibration Stimulus'
        self.vibrationSignal.description = 'Vibration Stimulus applied to the honey bee antenna'
        self.voltageSignal.name = 'Membrane Potential'
        self.voltageSignal.description = 'Vibration Sensitive inter-neuron membrane potential'

        raw_seg.analogsignals.append(self.vibrationSignal)
        raw_seg.analogsignals.append(self.voltageSignal)

        self.dataBlockToUpload.segments.append(raw_seg)

        self.mainSec = odml.Section(name=self.expName, type='experiment')
        expSummary = odml.Section(name=self.expName + '_Experiment', type='experiment/electrophysiology')

        freqVals = []
        expSummary.append(odml.Property(name='FrequenciesUsed', value=self.csvData['freqs']))
        expSummary.append(odml.Property(name='PulseInputDurations', value=self.csvData['pulse'][0]))
        expSummary.append(odml.Property(name='PulseInputIntervals', value=self.csvData['pulse'][1]))
        expSummary.append(odml.Property(name='SpontaneousActivityPresence', value=self.csvData['spont']))
        expSummary.append(odml.Property(name='NatureOfResponse', value=self.csvData['resp']))

        self.mainSec.append(expSummary)

        print 'Uploading metadata'
        secLoc = uploadNewSectionRecursive(self.GNodeSession, self.mainSec)
        print 'Uploading metadata Done'

        print 'Refreshing metadata'
        mainSec = self.GNodeSession.get(secLoc, refresh=True, recursive=True)
        for se in mainSec.sections:
            if se.name == self.expName + '_Experiment':
                self.dataBlockToUpload.section = se
                break
        print 'Refreshing metadata Done'

        print 'Uploading Data'
        blkLoc = uploadNewBlockRecursive(self.GNodeSession, self.dataBlockToUpload)
        print 'Uploading Data Done'

    #*******************************************************************************************************************

#***********************************************************************************************************************

