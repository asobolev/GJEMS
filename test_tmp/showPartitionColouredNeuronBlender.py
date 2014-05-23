import sys
sys.path.append('/home/ajay/repos/GJEMS/GJEMS/morph')

from blenderHelper import BlenderSWCImporter

print(sys.argv)
assert len(sys.argv) == 5, \
    'This script takes only 5 arguments, with the path of the swcfile expected as the 5th arguement, but ' \
        + str(len(sys.argv)) + ' found'
swcFName = sys.argv[4]


swcName = swcFName.rstrip('.swc')
ptSoma = False
if swcName[-8:] == '_3ptSoma':
    ptSoma = True
    swcName = swcName[:-8]

# partLabels = ['_AZ', '_DB', '_VB']
partLabels = ['-AZ', '-DB', '-VB']
cols = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
shouldAdd = False
blenderNrns = []

for partLabel, col in zip(partLabels, cols):

    if not ptSoma:
        partName = swcName + partLabel + '.swc'
    else:
        partName = swcName + partLabel + '_3ptSoma.swc'
    nrn = BlenderSWCImporter(partName, add=shouldAdd, matchRootOrigin=False)
    shouldAdd = True
    blenderNrns.append(nrn)
    nrn.importWholeSWC(col)


