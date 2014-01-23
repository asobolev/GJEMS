import numpy as np
from time import asctime
from neo import Segment, Block
import quantities as qu
import matplotlib.pyplot as plt
from scipy.signal import argrelmin, argrelmax
import gnodeclient
from .GNodeUpoadHelpers import *
import odml

#***********************************************************************************************************************

class RawDataProcessor():

    expName = None
    blockNameRaw = None
    blockNameProc = None
    mainSec = None
    GNodeSession = None
    maximumFreq = 700
    stimFreqs = None
    stimAmps = None
    stimDur = None
    stimInterval = None
    responseVTraces = None
    stimTraces = None
    extractedBlock = None
    voltageSignal = None
    vibrationSignal = None
    vibrationSignalDown = None
    vibrationSignalDownStdDev = None
    stimStartInds = None #at original sampling frequency, that of vibrationSignal
    stimEndInds = None #at original sampling frequency, that of vibrationSignal
    downSamplingFactor = None
    originalFile = None

    #*******************************************************************************************************************

    def downSampleVibSignal(self):

        self.downSamplingFactor = int(round(self.vibrationSignal.sampling_rate / (4 * self.maximumFreq)))
        newSamplingRate = self.vibrationSignal.sampling_rate / self.downSamplingFactor
        downSamplingIndices = range(0, len(self.vibrationSignal), self.downSamplingFactor)
        self.vibrationSignalDown = self.vibrationSignal[downSamplingIndices]
        self.vibrationSignalDown.sampling_rate = newSamplingRate

        self.vibrationSignalDown -= np.median(self.vibrationSignalDown)

        self.vibrationSignalDownStdDev = np.std(self.vibrationSignalDown)

    #*******************************************************************************************************************

    def __init__(self, expName):
        self.expName = expName
        self.blockNameRaw = expName + '_raw'
        self.blockNameProc = expName + '_proc'
        self.GNodeSession = gnodeclient.session.create(location="http://predata.g-node.org",
                                                       username="bob", password="pass")

        # ch = 'q'
        # if checkIfExists(self.GNodeSession, self.blockNameProc):
        #     ch = raw_input('A processed version of the input file exists on the server. \
        #                     Replace(r)/Do nothing and Quit(q)?:')
        #     if ch == 'r':
        #         deleteExistentBlock(self.GNodeSession, self.blockNameProc)
        #     else:
        #         cleanup(self.GNodeSession)
        #         sysexit()

    #*******************************************************************************************************************

    def checkExistenceOnServer(self):

        return checkIfExistsBlock(self.GNodeSession, self.blockNameProc)

    #*******************************************************************************************************************

    def deleteExistent(self):

        deleteExistentBlock(self.GNodeSession, self.blockNameProc)

    #*******************************************************************************************************************
    def getDataFromGNode(self):

        mainSec = self.GNodeSession.select(gnodeclient.Model.SECTION, {'name': self.expName})
        ent = 1
        if len(mainSec) > 1:
            ent = raw_input('More than one copies of the data found. Enter the serial number of the entry to use:')
        self.mainSec = self.GNodeSession.get(mainSec[ent - 1].location, recursive = True, refresh = True)

        subSec = self.mainSec.sections[self.expName + '_Experiment']
        dataBlock = subSec.blocks[0]
        # dataBlock = self.GNodeSession.get(blocks[0].location, refresh=True, recursive=True)
        self.originalFile = dataBlock.file_origin

        for analogSignal in dataBlock.segments[0].analogsignals:
            if analogSignal.name == 'Vibration Stimulus':
                self.vibrationSignal = analogSignal
            elif analogSignal.name == 'Membrane Potential':
                self.voltageSignal = analogSignal

    #*******************************************************************************************************************

    def plotVibEpoch(self, epochTimes, signal=None, points=False):

        # indStart = int(epochTimes[0] * qu.s * self.entireVibrationSignal.sampling_rate + self.recordingStartIndex)
        # indEnd = int(epochTimes[1] * qu.s * self.entireVibrationSignal.sampling_rate + self.recordingStartIndex)

        # epochTVec = self.entireVibrationSignal.t_start + np.arange(indStart, indEnd) * self.entireVibrationSignal.sampling_period

        # plt.plot(epochTVec, self.entireVibrationSignal[indStart:indEnd], 'g' + extra)

        indStart = int(epochTimes[0] * qu.s * self.vibrationSignalDown.sampling_rate)
        indEnd = int(epochTimes[1] * qu.s * self.vibrationSignalDown.sampling_rate)

        epochTVec = self.vibrationSignalDown.t_start + np.arange(indStart, indEnd) * self.vibrationSignalDown.sampling_period

        stimEnds = (np.array(self.stimEndInds)) / self.downSamplingFactor
        stimStarts = (np.array(self.stimStartInds)) / self.downSamplingFactor

        stimEndsPresent = [x * self.vibrationSignalDown.sampling_period + self.vibrationSignalDown.t_start
                           for x in stimEnds if indStart <= x <= indEnd]
        stimStartsPresent = [x * self.vibrationSignalDown.sampling_period + self.vibrationSignalDown.t_start
                             for x in stimStarts if indStart <= x <= indEnd]

        extra = ''
        if points:
            extra = '*-'

        plt.plot(epochTVec, self.vibrationSignalDown[indStart:indEnd], 'g' + extra)
        plt.stem(stimStartsPresent, np.ones(np.shape(stimStartsPresent)), 'k')
        plt.stem(stimEndsPresent, np.ones(np.shape(stimEndsPresent)), 'm')
        if not signal is None:
            plt.plot(epochTVec, signal[indStart:indEnd], 'r' + extra)

        plt.plot(epochTVec, 2 * self.vibrationSignalDownStdDev * np.ones(epochTVec.shape), 'y')

    #*******************************************************************************************************************

    def showPlot(self):

        plt.show(block=True)

    #*******************************************************************************************************************

    # def getStimulusEpochs(self):
    #     """
    #     Using direct thesholding of signal amplitude and adaptive threshold to determine a valid gap between stimuli.
    #     :return:
    #     """
    #     absStart = None
    #     encounteredEnd = None
    #     countSinceLastEnd = 0
    #     lastStayAboveThresh = 0
    #     prevVal = 0
    #     thresh = 2 * self.vibrationSignalDownStdDev
    #
    #     self.stimStartInds = []
    #     self.stimEndInds = []
    #
    #     for index, stimValue in zip(range(len(self.vibrationSignalDown)), np.abs(self.vibrationSignalDown)):
    #
    #         if absStart is None:
    #
    #             if (stimValue > thresh) and (prevVal < thresh):
    #                 absStart = index
    #
    #         else:
    #
    #             if encounteredEnd is None:
    #                 lastStayAboveThresh += 1
    #
    #             else:
    #                 countSinceLastEnd += 1
    #
    #             if (stimValue < thresh) and (prevVal > thresh):
    #                 encounteredEnd = index
    #
    #             if (stimValue > thresh) and (prevVal < thresh):
    #                 lastStayAboveThresh = 0
    #                 countSinceLastEnd = 0
    #                 encounteredEnd = None
    #
    #             if countSinceLastEnd > 3 * lastStayAboveThresh:
    #                 self.stimStartInds.append(absStart * self.downSamplingFactor + self.recordingStartIndex)
    #                 self.stimEndInds.append(encounteredEnd * self.downSamplingFactor + self.recordingStartIndex)
    #                 absStart = None
    #                 encounteredEnd = None
    #                 countSinceLastEnd = 0
    #                 lastStayAboveThresh = 0
    #
    #         prevVal = stimValue
    #
    #     self.stimStartInds = np.array(self.stimStartInds)
    #     self.stimEndInds = np.array(self.stimEndInds)

    #*******************************************************************************************************************

    def getStimulusEpochs(self):
        """
        Using direct thesholding of signal amplitude and adaptive threshold to determine a valid gap between stimuli.
        :return:
        """

        thresholdedSig = np.asarray(np.abs(self.vibrationSignalDown) > 2 * self.vibrationSignalDownStdDev, int)
        thresholdedSigDiff = np.diff(thresholdedSig)
        positiveEdges = np.where(thresholdedSigDiff == 1)[0]
        negativeEdges = np.where(thresholdedSigDiff == -1)[0]

        if negativeEdges[0] < positiveEdges[0]:
            negativeEdges = negativeEdges[1:]

        if positiveEdges[len(positiveEdges) - 1] > negativeEdges[len(negativeEdges) - 1]:
            positiveEdges = positiveEdges[:len(positiveEdges) - 1]

        staysAboveThreshold = negativeEdges[1:] - positiveEdges[1:]
        staysBelowThreshold = positiveEdges[1:] - negativeEdges[:len(negativeEdges) - 1]
        # for ind in range(500,550):
        #     print positiveEdges[1+ind],negativeEdges[ind],staysAboveThreshold[ind],staysBelowThreshold[ind]
        allEdges = [(n, p) for p, n, a, b in zip(positiveEdges[1:], negativeEdges[:len(negativeEdges) - 1],
                                                 staysAboveThreshold, staysBelowThreshold)
                    if b > 3 * a]

        self.stimStartInds = [positiveEdges[0]]
        self.stimEndInds = []

        for (end, start) in allEdges:
            self.stimStartInds.append(start)
            self.stimEndInds.append(end)

        self.stimEndInds.append(negativeEdges[len(negativeEdges) - 1])

        self.stimStartInds = np.array(self.stimStartInds) * self.downSamplingFactor
        self.stimEndInds = np.array(self.stimEndInds) * self.downSamplingFactor

        self.stimDur = (self.stimEndInds - self.stimStartInds) * self.vibrationSignal.sampling_period.simplified
        self.stimInterval = np.zeros(np.shape(self.stimDur))
        self.stimInterval[:len(self.stimInterval) - 1] = np.diff(self.stimStartInds) \
                                                        * self.vibrationSignal.sampling_period.simplified.magnitude
        self.stimInterval = qu.Quantity(self.stimInterval, self.vibrationSignal.sampling_period.simplified.units)

    #*******************************************************************************************************************

    def extractResponse(self):

        stimStarts = (self.stimStartInds) / self.downSamplingFactor
        stimEnds = (self.stimEndInds) / self.downSamplingFactor
        samplingRateDown = self.vibrationSignalDown.sampling_rate

        self.stimAmps = []
        self.stimFreqs = []
        self.responseVTraces = []
        self.stimTraces = []
        for (stD, endD, st, end) in zip(stimStarts, stimEnds, self.stimStartInds, self.stimEndInds):

            stimDown = self.vibrationSignalDown[stD:endD + 1]
            stimDownFFT = np.fft.rfft(stimDown, n=2048)
            self.stimFreqs.append(np.argmax(np.abs(stimDownFFT)) * samplingRateDown / 2 / len(stimDownFFT))

            stimAS = self.vibrationSignal[st:end + 1]
            stim = stimAS.magnitude
            allAmps = stim[np.concatenate((argrelmin(stim)[0], argrelmax(stim)[0]))]

            self.stimAmps.append(np.abs(allAmps).mean() * self.vibrationSignal.units)

            self.responseVTraces.append(self.voltageSignal[st:end + 1])

            self.stimTraces.append((stimAS - np.mean(stimAS)))

    #*******************************************************************************************************************

    def getSegment(self, ind=0):

        stim = self.stimTraces[ind]
        resp = self.responseVTraces[ind]
        freq = self.stimFreqs[ind]
        amp = self.stimAmps[ind]

        tVec = (np.arange(len(stim)) + self.stimStartInds[ind]) * self.vibrationSignal.sampling_period
        plt.plot(tVec, stim, 'b')
        plt.plot(tVec, resp, 'r')
        inter = (np.array([self.stimStartInds[ind], self.stimEndInds[ind]])) * self.vibrationSignal.sampling_period.simplified
        plt.title('Freq=' + str(np.round(freq, 2)) + ',  Amp=' + str(np.round(amp, 2)) + ',  Interval=' + str(np.round(inter, 2)))
        plt.axis('off')

    #*******************************************************************************************************************

    def uploadToGNode(self):

        blk = Block()
        blk.name = self.blockNameProc
        blk.file_origin = self.originalFile
        blk.file_datetime = asctime()
        blk.description = 'Regions of Interest of electrophysiological recordings of a vibration sensitive neuron'
        blk = self.GNodeSession.set(blk)

        expSec = self.mainSec.sections[self.expName + '_Experiment']
        freqProp = expSec.properties['FrequenciesUsed']
        writtenFreq = getValuesOfProperty(freqProp)
        durProp = expSec.properties['PulseInputDurations']
        writtenDur = getValuesOfProperty(durProp)
        intervalProp = expSec.properties['PulseInputIntervals']
        writtenIntervals = getValuesOfProperty(intervalProp)

        blk.section = expSec
        blk = self.GNodeSession.set(blk)

        count = 0
        for (freq, amp, resp, stim, dur, inter) in \
            zip(self.stimFreqs, self.stimAmps, self.responseVTraces, self.stimTraces, self.stimDur, self.stimInterval):

            count += 1

            print 'Uploading Segment' + str(count)
            seg = self.GNodeSession.set(Segment(name=blk.name + '_seg' + str(count), index=count))

            seg.block = blk
            seg = self.GNodeSession.set(seg)

            resp.name = 'Membrane Potential'
            resp.description = 'Response to the associated vibration stimulus applied to the antenna.'
            stim.name = 'Vibration Stimulus'
            stim.description = 'Vibration Stimulus applied to the antenna'

            resp = self.GNodeSession.set(resp)
            stim = self.GNodeSession.set(stim)

            resp.segment = seg
            stim.segment = seg

            resp = self.GNodeSession.set(resp)
            stim = self.GNodeSession.set(stim)

            metadata = []

            metadata.append(freqProp.values[find_nearest_Id(writtenFreq, freq)])
            if min(abs(writtenDur - dur)).magnitude < 5:
                metadata.append(durProp.values[find_nearest_Id(writtenDur, dur)])
                metadata.append(intervalProp.values[find_nearest_Id(writtenIntervals, inter)])

            seg.metadata = metadata
            seg = self.GNodeSession.set(seg)

            print 'Uploading Segment' + str(count) + ' Done'
            import ipdb
            ipdb.set_trace()

    #*******************************************************************************************************************

#***********************************************************************************************************************


