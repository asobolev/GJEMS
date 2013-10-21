import neuron as nrn
import pkgutil


class MorphImport:

    rootPtr = None
    nTips = 0
    tipPtrs = []
    cell = None
    totalSections = 0
    allsec = []
    nrnT = nrn.h.Vector()
    regionMarkSecs = None
    branchPointSec = None
    packagePrefix = pkgutil.get_loader("GJMorphSim").filename + '/'


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
    
    def setRegionIndex(self, subtreeIndex, secPtr):
	
	secPtr.sec().regionInd.index = subtreeIndex
	
	if secPtr.nchild() == 0:
	  
	    return 
	  
	else:
	  
	    for childId in range(int(secPtr.nchild())):
		
		childPtr = self.getPtr(secPtr.child[childId])
		self.setRegionIndex(subtreeIndex, childPtr)
		
	    return  

    
    #*******************************************************************************************************************

    def setRegionIndex(self, subtreeIndex, secPtr):

        secPtr.sec().regionInd.index = subtreeIndex

        if secPtr.nchild() == 0:

            return

        else:

            for childId in range(int(secPtr.nchild())):

                childPtr = self.getPtr(secPtr.child[childId])
                self.setRegionIndex(subtreeIndex, childPtr)

            return

    #*******************************************************************************************************************

    def initRegionIndices(self,marksFile):

        marksFle = open(marksFile, 'r')


        #skip commented lines
        tempStr = '#'
        startChar = tempStr[0]
        while (startChar == '#') or (startChar == '\n'):
            tempStr = marksFle.readline()
            startChar = tempStr[0]

        tempStr = tempStr.rstrip('\n')
        marksFle.close()
        tempWords = tempStr.split('\t')
        branchPointMark = tempWords[0]
        regionMarks = tempWords[1:4]
        self.regionMarkSecs = [0] * 3
        regionMarksDone = 0

        for sec in self.allsec:

            secName = sec.name()
            if secName == branchPointMark:
                self.branchPointSec = sec
            elif (secName in regionMarks) and (regionMarksDone < 3):
                self.regionMarkSecs[regionMarks.index(secName)] = sec

        for sec in self.regionMarkSecs:
            self.setRegionIndex(self.regionMarkSecs.index(sec)+1, self.getPtr(sec))


    #*******************************************************************************************************************

    def __init__(self, morphFile):

        nrn.h.xopen(self.packagePrefix+'etc/import3D_batch.hoc')
        self.cell = nrn.h.mkcell(morphFile)

        nrn.load_mechanisms(self.packagePrefix+'etc')


        self.rootPtr = self.getRootPtr()

        self.getTipPtrs(self.rootPtr)
        
        for sec in self.allsec:
            sec.insert('regionInd')

        
        
        self.initRegionIndices(morphFile.rstrip('.swc')+'.marks')

        for sec in self.allsec:
            sec.insert('regionInd')

        self.initRegionIndices(morphFile.rstrip('.swc') + '.marks')

    #*******************************************************************************************************************