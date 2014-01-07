from GJMorphSim.ephys.rawDataProcess import *
import time
import matplotlib.pyplot as plt
import ipdb
import easygui
from easygui import fileopenbox, ynbox, msgbox

upload = True
see = RawDataProcessor('131018-1Al')
if see.checkExistenceOnServer():
    upload = ynbox('This data already exists on the server. Replace the data?')
    if upload:
        print 'Deleting Existing Data'
        see.deleteExistent()
    else:
        msgbox('Data on the server not replaced')

if upload:
    see.getDataFromGNode()
    # ipdb.set_trace()
    see.downSampleVibSignal()
    # ipdb.set_trace()
    see.getStimulusEpochs()
    # ipdb.set_trace()
    see.extractResponse()
    # ipdb.set_trace()
    see.uploadToGNode()


# plt.figure();plt.show(block=False)
# for respInd in range(len(see.responseVTraces)):
#     plt.cla()
#     see.getSegment(respInd)
#     plt.draw()
#     ch = 'n'
#     ch = raw_input('Next(n)/Quit(q):')
#     if ch == 'q':
#         break

