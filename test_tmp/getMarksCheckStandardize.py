import subprocess
import sys
import os
import shutil

def getMarksFileName(swcFName):

    return swcFName[:-4] + '.marks'

assert len(sys.argv) == 2, 'Only one argument, the path of the swcfile expected, ' + str(len(sys.argv)) + 'found'
swcfName = sys.argv[1]

swcDir, swcName = os.path.split(swcfName)
outerSWCfName = os.path.join(os.path.split(swcDir)[0], swcName)


if not os.path.isfile(getMarksFileName(swcfName)):
    subprocess.call(['python', 'getMarksFile.py', swcfName])
retCode = subprocess.call(['python', 'showPartitionColouredNeuron.py', swcfName])

if retCode:
    print('Improper Partitioning!')
    sys.exit()

else:

    shutil.copy(swcfName, outerSWCfName)
    shutil.copy(getMarksFileName(swcfName), getMarksFileName(outerSWCfName))

    subprocess.call(['python', 'standardizeSWCFull.py', outerSWCfName])
    subprocess.call(['python', 'standardizeSWCUAlign.py', outerSWCfName])

