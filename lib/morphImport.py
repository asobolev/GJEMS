import neuron as nrn


class MorphImport:

    rootPtr = None
    nTips = 0
    tipPtrs = []
    cell = None
    totalSections = 0
    allsec = []
    nrnT = nrn.h.Vector()

    #*******************************************************************************************************************

    def getPtr(self, sec):

        sec.push()
        ptr = nrn.h.SectionRef()
        nrn.h.pop_section()
        return ptr

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

    def initRegionIndices(self,marksFile):

        marksFle = open(marksFile, 'r')
        tempStr = marksFle.readline()
        marksFle.close()

        regionMarks = tempStr.split('\t')


    #*******************************************************************************************************************

    def __init__(self, morphFile):

        nrn.h.xopen('../etc/import3D_batch.hoc')
        self.cell = nrn.h.mkcell(morphFile)
        nrn.load_mechanisms('../etc')

        for sec in self.allsec:
            sec.insert('regionInd')

        self.rootPtr = self.getRootPtr()

        self.getTipPtrs(self.rootPtr)

    #*******************************************************************************************************************