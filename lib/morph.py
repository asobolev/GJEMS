import neuron as nrn
import os
# import matplotlib.pyplot as plt
# import numpy as npy

#TODO: LMFilter class to support Specificity feature of L-measure

class LMIO:
    
    LMPath = '../Lm/'
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


    line1 = ""
    line2 = ""
    line3 = ""

    def __init__(self, morphFile):

        self.line3 = morphFile
        
    def writeLMIn(self,line1,line2,line3):
	
	LMInputFName = '../tmp/LMInput'
	LMIn = open(LMInputFName,'w')
        LMIn.write(line1+'\n'+line2+'\n'+line3)
        LMIn.close()
        return LMInputFName
      
    def runLM(self,LMInputFName):
	
	os.system(''+self.LMPath+'')

    def getMeasureDistribution(self, measure, average=False, nBins=10, Filter=False):

        self.line1 = '-f' + str(self.functionRef.index(measure)) + ',' + str(int(average)) + ',0,' + str(nBins)

        self.line2 = '-s../tmp/LMOutput'
        
        LMInputFName = writeLMIn(self.line1,self.line2,self.line3)
     





class BasicMorph:

    rootPtr = None
    nTips = 0
    tipPtrs = []
    cell = None
    totalSections = 0
    allsec = []
    swcFile = None

    #*******************************************************************************************************************

    def getPtr(self, sec):

        sec.push()
        ptr = nrn.h.SectionRef()
        nrn.h.pop_section()
        return ptr

    #*******************************************************************************************************************

    #*******************************************************************************************************************

    def getRootPtr(self):

        tempPtr = nrn.h.SectionRef()
        tempPtr.root().sec.push()
        rootPtr = nrn.h.SectionRef()
        nrn.h.pop_section()
        return rootPtr

    #*******************************************************************************************************************


    def getTipPtrs(self, presentPtr):

        self.totalSections += 1
        self.allsec.append(presentPtr.sec)

        if presentPtr.nchild() == 0:

            self.nTips += 1
            self.tipPtrs.append(presentPtr)
            return

        else:
            for childId in range(int(presentPtr.nchild())):
                childPtr = self.getPtr(presentPtr.child[childId])
                self.getTipPtrs(childPtr)
            return

    #*******************************************************************************************************************

    def __init__(self, morphFile):

        self.swcFile = morphFile

        nrn.h.xopen('../etc/import3D_batch.hoc')
        self.cell = nrn.h.mkcell(morphFile)

        self.rootPtr = self.getRootPtr()

        self.getTipPtrs(self.rootPtr)

    #*******************************************************************************************************************