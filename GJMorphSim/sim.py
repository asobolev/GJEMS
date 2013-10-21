import matplotlib.pyplot as plt
import numpy as npy
from morphImport import MorphImport
import neuron as nrn

def showPlot():

    plt.show(block=True)


class VoltageRecord:

    nrnVVecName = None
    vVec = None

    def __init__(self, sec, where):

        assert (where <= 1  and where >= 0), 'variable \'where\' has to be in [0,1]'

        secName = sec.name()
        secName = secName.replace('[', '')
        secName = secName.replace(']', '')
        secName = secName.replace('.', '')

        self.nrnVVecName = secName + 'VVec'
        nrn.h('objref ' + self.nrnVVecName)
        nrn.h(self.nrnVVecName + ' = new Vector()')
        nrn.h(self.nrnVVecName + '.record(&' + sec.name() + '.v(' + str(where) + '))')

        # print self.nrnVVecName + '.record(&' + sec.name() + '.v(' + str(where) + '))'

    def plotSeparately(self, tVec):

        exec('self.vVec = nrn.h.' + self.nrnVVecName + '.as_numpy()')

        assert len(self.vVec) == len(tVec)

        fig1 = plt.figure()
        plt.plot(tVec, self.vVec, color='r')

        plt.draw()

        return fig1

    def addPlotToFig(self, tVec, fig, col='b'):

        plt.figure(fig.number)

        exec('self.vVec = nrn.h.' + self.nrnVVecName + '.as_numpy()')

        assert len(self.vVec) == len(tVec)

        plt.plot(tVec, self.vVec, c=col)

        plt.draw()

    def toNumpy(self):

        exec('self.vVec = nrn.h.' + self.nrnVVecName + '.as_numpy()')


#***********************************************************************************************************************

class SpikeRecord:

    nrnSpVec = nrn.h.Vector()
    spVec=[]

    def __init__(self,  seg, vThresh):
        nrnAPC = nrn.h.APCount(seg) #TODO check if this works and modify if required
        nrnAPC.thresh = vThresh
        nrnAPC.record(self.nrnSpVec)


    def toPython(self):

        self.spVec = npy.zeros([int(self.nrnSpVec.size()),1])
        self.nrnSpVec.to_python(self.spVec)

#***********************************************************************************************************************


class BasicSim(MorphImport):

    cmDefault = 1
    RaDefault = 100
    nsegDefault = 10
    RmDefault = 30e3
    e_pasDefault = -65

    def __init__(self, morphFile, dt=0.025, tstop=1000):

        MorphImport.__init__(self, morphFile=morphFile)

        nrn.h.dt = dt
        self.tStop = tstop
        self.nrnT.record(nrn.h._ref_t)

        #set default intrinsic and passive section parameters.
        for sec in self.allsec:

            sec.cm = self.cmDefault
            sec.Ra = self.RaDefault
            sec.nseg=self.nsegDefault

            sec.insert('pas')
            sec.e_pas = self.e_pasDefault
            sec.g_pas = 1/self.RmDefault

    #*******************************************************************************************************************


    def setUniformPas(self , e_pas , g_pas):

        for sec in self.allsec:
            sec.e_pas = e_pas
            sec.g_pas = g_pas

    #*******************************************************************************************************************

    def setSimProps(self, dt=0.025 , tstop=1000):

        nrn.h.dt = dt
        self.tStop = tstop

    #*******************************************************************************************************************

    def placeRootIClamp(self, amp, dur, delay=0):

        iClamp = nrn.h.IClamp(self.rootPtr.sec(0.5))

        iClamp.amp = amp
        iClamp.dur = dur
        iClamp.delay = delay

        return iClamp

    #*******************************************************************************************************************

    def placeTipIClamp(self, tipPtr, amp, dur, delay=0):

        iClamp = nrn.h.IClamp(tipPtr.sec(0.5))

        iClamp.amp = amp
        iClamp.dur = dur
        iClamp.delay = delay

        return iClamp

    #*******************************************************************************************************************

    def placeAllTipIClamp(self, amp, dur, delay=0):

        tipIClamps = []

        for tipPtr in self.tipPtrs:

            iClamp = nrn.h.IClamp(tipPtr.sec(0.5))

            iClamp.amp = amp
            iClamp.dur = dur
            iClamp.delay = delay

            tipIClamps.append(iClamp)

        return tipIClamps

    #*******************************************************************************************************************

    def recordRootVoltage(self):

        rootVRecord = VoltageRecord(self.rootPtr.sec, 0.5)

        return rootVRecord

    #*******************************************************************************************************************

    def recordTipVoltage(self, tipPtr):

        tipVRecord = VoltageRecord(tipPtr.sec, 0.5)

        return tipVRecord

    #*******************************************************************************************************************

    def recordAllTipsVoltages(self):

        tipVRecords = []

        for tipPtr in self.tipPtrs:

            tipVRecord = VoltageRecord(tipPtr.sec, 0.5)

            tipVRecords.append(tipVRecord)

        return tipVRecords

    #*******************************************************************************************************************

    def initAndRun(self,reset_V = -65):

        nrn.h.finitialize(reset_V)
        nrn.init()
        nrn.run(self.tStop)

    #*******************************************************************************************************************

    def getTimeVec(self):

        tVec= [0]*int(self.nrnT.size())
        self.nrnT.to_python(tVec)

        return tVec

    #*******************************************************************************************************************

#***********************************************************************************************************************

