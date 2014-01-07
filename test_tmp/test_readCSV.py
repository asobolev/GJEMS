from GJMorphSim.ephys import *
import time
from easygui import fileopenbox

smr = fileopenbox('Indicate the smr file to use', filetypes=['*.smr'])
testEphys = BasicEphys(smr, 'spike2Files/Neuron_Database.csv')
testEphys.parseCSV()
print testEphys.csvData
