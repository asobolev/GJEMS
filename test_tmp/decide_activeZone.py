from GJMorphSim.morph import *
from easygui import fileopenbox
# import numpy as npy


testMorphFile = fileopenbox(msg='SWC file with single point soma', filetypes=['*.swc'])

testMorph = BasicMorph(morphFile=testMorphFile, initDists=True)

for childId in range(int(testMorph.rootPtr.nchild())):
    child = testMorph.rootPtr.child[childId]

    if child.name().find('dend') > 0:
        branchPtr = testMorph.getPtr(child)

nchild = int(branchPtr.nchild())
while nchild == 1:
    branchPtr = testMorph.getPtr(branchPtr.child[0])
    nchild = int(branchPtr.nchild())


subtreeDir = testMorph.morphFilePath + testMorph.morphFileName.rstrip('.swc') + '_subTrees'
if not os.path.isdir(subtreeDir):
    os.mkdir(subtreeDir)

subtrees = []
for childId in range(int(branchPtr.nchild())):

    subTreeName = subtreeDir + '/' + testMorph.morphFileName.rstrip('.swc') + \
                  '_' + str(childId) + '.swc'

    regionSWCwriter = SubTreeWriter(testMorph.getPtr(branchPtr.child[childId]))
    regionSWCwriter.write(subTreeName)




