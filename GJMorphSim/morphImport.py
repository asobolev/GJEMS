import neuron as nrn
import pkgutil
import numpy as npy
import os


class SubTreeWriter:

    rootSecPtr = None
    swcFileList = []
    pointsDone = 0

    def __init__(self, secPtr):

        self.rootSecPtr = secPtr

    #*******************************************************************************************************************

    def getPtr(self, sec):

        sec.push()
        ptr = nrn.h.SectionRef()
        nrn.h.pop_section()
        return ptr

    #*******************************************************************************************************************
    def getSectionxyzd(self, secPtr):

        xyzd = []
        secPtr.sec.push()
        for pointInd in range(int(nrn.h.n3d())):
            temp = [nrn.h.x3d(pointInd), nrn.h.y3d(pointInd), nrn.h.z3d(pointInd), nrn.h.diam3d(pointInd)]
            xyzd.append(temp)
        nrn.h.pop_section()
        return xyzd

    #*******************************************************************************************************************

    def addLine(self, xyzd, pointType, parent):

        self.pointsDone += 1

        swcLine = [self.pointsDone, pointType]
        swcLine.extend(xyzd)
        swcLine.append(parent)
        self.swcFileList.append(swcLine)


    #*******************************************************************************************************************

    def addSubTreeSWC(self, parent, secPtr):

        xyzd = self.getSectionxyzd(secPtr)

        for pointInd in range(len(xyzd)):

            # if the present point is the origin of subtree, it is defined a three point soma

            if (parent == -1) and (pointInd == 0):


                somaXYZD = xyzd[0]

                rs = somaXYZD[3]

                soma1XYZD = [x for x in somaXYZD]
                soma1XYZD[1] += rs

                soma2XYZD = [x for x in somaXYZD]
                soma2XYZD[1] -= rs

                self.addLine(somaXYZD, 1, -1)

                self.addLine(soma1XYZD, 1, 1)

                self.addLine(soma2XYZD, 1, 1)

                parent = 1

            else:

                self.addLine(xyzd[pointInd], 3, parent)

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
        npy.savetxt(fName, self.swcFileList, '%d %d %0.12f %0.12f %0.12f %0.12f %d')


    #*******************************************************************************************************************



class MorphImport:

    morphFilePath = ''
    morphFileName = ''
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
    writtenPoints = []
    subTreesLabels = ['db','vb','ppl']
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

    def initRegionIndices(self, marksFile):

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
            self.setRegionIndex(self.regionMarkSecs.index(sec) + 1, self.getPtr(sec))

    #*******************************************************************************************************************

    def saveSubtrees(self):

        subtreeDir = self.morphFilePath + self.morphFileName.rstrip('.swc') + '_subTrees'
        if not os.path.isdir(subtreeDir):
            os.mkdir(subtreeDir)

        for subTreeInd in range(len(self.regionMarkSecs)):

            subTreeName = subtreeDir + '/' + self.morphFileName.rstrip('.swc') +\
                           '_' + self.subTreesLabels[subTreeInd] + '.swc'

            self.subTreeSWCPaths.append(subTreeName)

            regionSWCwriter = SubTreeWriter(self.getPtr(self.regionMarkSecs[subTreeInd]))
            regionSWCwriter.write(subTreeName)

    #*******************************************************************************************************************

    def initDistances(self):

        self.sec0dists = []
        self.sec1dists = []

        for sec in self.allsec:

            sec.push()
            self.sec0dists.append(nrn.h.distance(0))
            self.sec1dists.append(nrn.h.distance(1))
            nrn.h.pop_section()

    #*******************************************************************************************************************
    def __init__(self, morphFile):

        fNameWords = morphFile.rsplit('/')

        self.morphFileName = fNameWords[len(fNameWords)-1]

        for ind in range(len(fNameWords)-1):
            self.morphFilePath += (fNameWords[ind]+'/')


        nrn.h.xopen(self.packagePrefix+'etc/import3D_batch.hoc')
        self.cell = nrn.h.mkcell(morphFile)

        nrn.load_mechanisms(self.packagePrefix + 'etc')

        self.rootPtr = self.getRootPtr()

        self.getTipPtrs(self.rootPtr)

        for sec in self.allsec:
            sec.insert('regionInd')

    #*******************************************************************************************************************