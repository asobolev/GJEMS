import neuron as nrn
import numpy as npy
import os


class SubTreeWriter:

    rootSecPtr = None
    swcFileList = []
    pointsDone = 0

    def __init__(self, secPtr, extraColFunc=None):

        self.rootSecPtr = secPtr
        self.extraColFunc = extraColFunc

    #*******************************************************************************************************************

    def getPtr(self, sec):

        sec.push()
        ptr = nrn.h.SectionRef()
        nrn.h.pop_section()
        return ptr

    #*******************************************************************************************************************
    def getSectionxyzr(self, secPtr):

        xyzr = []
        secPtr.sec.push()
        for pointInd in range(int(nrn.h.n3d())):
            temp = [nrn.h.x3d(pointInd), nrn.h.y3d(pointInd), nrn.h.z3d(pointInd), 0.5 * nrn.h.diam3d(pointInd)]
            xyzr.append(temp)
        nrn.h.pop_section()
        return xyzr

    #*******************************************************************************************************************

    def addLine(self, xyzr, pointType, parent, secPtr):

        self.pointsDone += 1

        swcLine = [self.pointsDone, pointType]
        swcLine.extend(xyzr)
        swcLine.append(parent)

        if self.extraColFunc is not None:

            extraCols = self.extraColFunc(secPtr)
            swcLine.extend(extraCols)


        self.swcFileList.append(swcLine)

    #*******************************************************************************************************************

    def addSubTreeSWC(self, parent, secPtr):

        xyzr = self.getSectionxyzr(secPtr)

        for pointInd in range(len(xyzr) - 1):

            # if the present point is the origin of subtree, it is defined as a three point soma

            if (parent == -1) and (pointInd == 0):

                somaXYZD = xyzr[0]

                rs = somaXYZD[3]

                soma1XYZD = [x for x in somaXYZD]
                soma1XYZD[1] += rs

                soma2XYZD = [x for x in somaXYZD]
                soma2XYZD[1] -= rs

                self.addLine(somaXYZD, 1, -1, secPtr)

                self.addLine(soma1XYZD, 1, 1, secPtr)

                self.addLine(soma2XYZD, 1, 1, secPtr)

                parent = 1

            else:

                self.addLine(xyzr[pointInd], 3, parent, secPtr)

                #Note: present value of self.pointsDone == parents column 1 entry
                parent = self.pointsDone

        if secPtr.nchild() == 0:

            return

        else:

            for childId in range(int(secPtr.nchild())):

                self.addSubTreeSWC(parent, self.getPtr(secPtr.child[childId]))

            return

    #*******************************************************************************************************************

    def write(self, fName):

        self.swcFileList = []
        self.pointsDone = 0
        self.addSubTreeSWC(-1, self.rootSecPtr)
        formatString = '%d %d %0.3f %0.3f %0.3f %0.3f %d'

        if self.extraColFunc is not None:

            extraColsSample = self.extraColFunc(self.rootSecPtr)
            for ind in range(len(extraColsSample)):
                formatString += ' %d'

        npy.savetxt(fName, self.swcFileList, formatString)


    #*******************************************************************************************************************


class MorphImport:

    morphFilePath = ''
    morphFileName = ''
    rootPtr = None
    nTips = 0
    cell = None
    totalSections = 0
    nrnT = nrn.h.Vector()
    regionMarkSecs = None
    branchPointSec = None
    packagePrefix = os.path.split(os.path.split(__file__)[0])[0]
    writtenPoints = []
    subTreesLabels = ['db', 'vb']
    subTreeSWCPaths = []
    sec0dists = []
    sec1dists = []

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
        nrn.h.distance()
        nrn.h.pop_section()

        return rootPtr

    #*******************************************************************************************************************

    def getSectionxyzr(self, secPtr):

        xyzr = []
        secPtr.sec.push()
        for pointInd in range(int(nrn.h.n3d())):
            temp = [nrn.h.x3d(pointInd), nrn.h.y3d(pointInd), nrn.h.z3d(pointInd), 0.5 * nrn.h.diam3d(pointInd)]
            xyzr.append(temp)
        nrn.h.pop_section()
        return xyzr

    #*******************************************************************************************************************

    def getTipPtrs(self, presentPtr):

        self.totalSections += 1
        self.allsec[presentPtr.sec.name()] = presentPtr.sec

        if presentPtr.nchild() == 0:

            self.nTips += 1
            self.tipPtrs[presentPtr.sec.name()] = presentPtr
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

    def initRegionIndices(self, marksFile):

        nrn.load_mechanisms(os.path.join(self.packagePrefix, 'etc'))

        for sec in self.allsec.values():
            sec.insert('regionInd')

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
        regionMarks = tempWords[1:len(self.subTreesLabels) + 1]

        self.regionMarkSecs = [0] * len(self.subTreesLabels)
        regionMarksDone = 0

        for secName, sec in self.allsec.iteritems():

            secName = sec.name()
            if secName == branchPointMark:
                self.branchPointSec = sec
            elif (secName in regionMarks) and (regionMarksDone < len(self.subTreesLabels)):
                self.regionMarkSecs[regionMarks.index(secName)] = sec
                regionMarksDone += 1

        for secInd in range(len(self.regionMarkSecs)):
            regionMarkSectionPtr = self.getPtr(self.regionMarkSecs[secInd])
            self.setRegionIndex(secInd + 1, regionMarkSectionPtr)
            #include the demarkating section in the active zone.
            regionMarkSectionPtr.sec().regionInd.index = 0


    #*******************************************************************************************************************

    def saveSubtrees(self):

        subtreeDir = os.path.join(self.morphFilePath, self.morphFileName.rstrip('.swc') + '_subTrees')
        if not os.path.isdir(subtreeDir):
            os.mkdir(subtreeDir)

        for subTreeInd in range(len(self.regionMarkSecs)):

            subTreeName = os.path.join(subtreeDir, self.morphFileName.rstrip('.swc') +
                           '_' + self.subTreesLabels[subTreeInd] + '.swc')

            self.subTreeSWCPaths.append(subTreeName)

            regionSWCwriter = SubTreeWriter(self.getPtr(self.regionMarkSecs[subTreeInd]))
            regionSWCwriter.write(subTreeName)

    #*******************************************************************************************************************
    def __init__(self, morphFile):

        self.tipPtrs = {}
        self.allsec = {}

        (self.morphFilePath, self.morphFileName) = os.path.split(morphFile)

        if not 'mkcell' in dir(nrn.h):
            nrn.h.xopen(os.path.join(self.packagePrefix, 'etc/import3D_batch.hoc'))

        self.cell = nrn.h.mkcell(morphFile)

        self.rootPtr = self.getRootPtr()

        self.getTipPtrs(self.rootPtr)



    #*******************************************************************************************************************