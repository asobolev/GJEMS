import neuron as nrn
# import matplotlib.pyplot as plt
# import numpy as npy



def getTipPtrs(self, presentPtr):

    self.totalSections += 1
    self.allsec.append(presentPtr.sec)

    if presentPtr.nchild() == 0:

        self.nTips += 1
        self.tipPtrs.append(presentPtr)
        return

    else:
        for childId in range(int(presentPtr.nchild())):
            childPtr = getPtr(presentPtr.child[childId])
            self.getTipPtrs(childPtr)
        return


class BasicMorph:

    rootPtr = None
    nTips = 0
    tipPtrs = []
    cell = None
    totalSections = 0
    allsec = []

    #*******************************************************************************************************************

    def getPtr(self, sec):

        sec.push()
        ptr = nrn.h.SectionRef()
        nrn.h.pop_section()
        return ptr

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
        nrn.h.xopen('../etc/import3D_batch.hoc')
        self.cell = nrn.h.mkcell(morphFile)

        tempPtr = nrn.h.SectionRef()
        tempPtr.root().sec.push()
        self.rootPtr = nrn.h.SectionRef()
        nrn.h.pop_section()

        self.getTipPtrs(self.rootPtr)

    #*******************************************************************************************************************