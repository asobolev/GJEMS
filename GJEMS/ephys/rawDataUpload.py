import os
from neo import Spike2IO, Segment, Block
import quantities as qu
import gnodeclient
from .GNodeUpoadHelpers import *
import odml
import csv
from time import asctime

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

    csvData['freqs'] = [float(x) * qu.Hz for x in lne[freqCol].split(',') if not x == '']

    if not lne[pulseCol] == '':
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
            lastNum = csvData['pulse'][0][-1]
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

    #*******************************************************************************************************************

    def __init__(self, ephysFile, csvFile, username, password, location="http://predata.g-node.org"):

        assert os.path.isfile(ephysFile), 'SMR file not found'
        assert os.path.isfile(csvFile), 'csv file not found'

        self.ephysFile = ephysFile
        self.expName = os.path.split(ephysFile)[1].strip('.smr')
        self.blockName = self.expName + '_raw'
        self.csvFile = csvFile
        self.session = gnodeclient.session.create(
            location=location, username=username, password=password
        )
        spike2Reader = Spike2IO(self.ephysFile)
        self.dataBlock = spike2Reader.read()[0]

    #*******************************************************************************************************************

    def checkExistenceOnServer(self):

        return checkIfExistsSection(self.session, self.expName)

    #*******************************************************************************************************************

    def deleteExistent(self):

        deleteExistentBlock(self.session, self.blockName)
        deleteExistentSection(self.session, self.expName)

    #*******************************************************************************************************************

    def parseSpike2Data(self):

        entireVoltageSignal = self.dataBlock.segments[0].analogsignals[0]
        entireVibrationSignal = self.dataBlock.segments[0].analogsignals[1]

        if len(self.dataBlock.segments[0].analogsignals) > 2:
                entireCurrentSignal = self.dataBlock.segments[0].analogsignals[2]


        recordingStartTime = max(entireVibrationSignal.t_start, entireVoltageSignal.t_start)
        recordingEndTime = min(entireVibrationSignal.t_stop, entireVoltageSignal.t_stop)

        recordingStartTime = self.dataBlock.segments[0].eventarrays[0].times[0]
        recordingEndTime = self.dataBlock.segments[0].eventarrays[0].times[1]

        recordingStartIndex = int((recordingStartTime - entireVoltageSignal.t_start)
                                  * entireVoltageSignal.sampling_rate)
        recordingEndIndex = int((recordingEndTime - entireVoltageSignal.t_start) * entireVoltageSignal.sampling_rate)

        self.vibrationSignal = entireVibrationSignal[recordingStartIndex:recordingEndIndex + 1] * 27.2 * qu.um
        self.voltageSignal = entireVoltageSignal[recordingStartIndex:recordingEndIndex + 1] * 20 * qu.mV

        if len(self.dataBlock.segments[0].analogsignals) > 2:
            self.currentSignal = entireCurrentSignal[recordingStartIndex:recordingEndIndex + 1] * qu.nA

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

        if len(self.dataBlock.segments[0].analogsignals) > 2:

            self.currentSignal.name = 'Current Signal'
            self.currentSignal.description = 'Indicates whether a current is being injected or not. The magnitudes ' \
                                             'are given in an event array'

            raw_seg.analogsignals.append(self.currentSignal)

            if len(self.dataBlock.segments[0].eventarrays) == 2:
                raw_seg.eventarrays.append(self.dataBlock.segments[0].eventarrays[1])

        self.dataBlockToUpload.segments.append(raw_seg)

        self.doc = odml.Document(author="Ajayrama K.", version="1.0")

        self.mainSec = odml.Section(name=self.expName, type='experiment')
        self.doc.append(self.mainSec)

        expSummary = odml.Section(name='VibrationStimulus', type='experiment/electrophysiology')

        if not self.csvData['freqs'] == []:
            expSummary.append(odml.Property(name='FrequenciesUsed', value=self.csvData['freqs']))

        if not self.csvData['pulse'][0] == []:
            expSummary.append(odml.Property(name='PulseInputDurations', value=self.csvData['pulse'][0]))

        if not self.csvData['pulse'][1] == []:
            expSummary.append(odml.Property(name='PulseInputIntervals', value=self.csvData['pulse'][1]))

        expSummary.append(odml.Property(name='SpontaneousActivityPresence', value=self.csvData['spont']))

        if not self.csvData['resp'] == '':
            expSummary.append(odml.Property(name='NatureOfResponse', value=self.csvData['resp']))

        self.mainSec.append(expSummary)

        print asctime() + ' : Uploading metadata'
        section = self.session.set_all(self.doc)
        print asctime() + ' : Uploading metadata Done'

        print asctime() + ' : Refreshing metadata'
        mainSec = self.session.get(section.location, refresh=True, recursive=True)
        print asctime() + ' : Refreshing metadata Done'

        self.dataBlockToUpload.section = mainSec

        print asctime() + ' : Uploading Data'
        blkLoc = self.session.set_all(self.dataBlockToUpload)
        print asctime() + ' : Uploading Data Done'

    #*******************************************************************************************************************

#***********************************************************************************************************************
