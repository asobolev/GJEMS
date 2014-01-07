from GJMorphSim.ephys.rawDataProcess import *
import time
import matplotlib.pyplot as plt
import ipdb

see = RawDataProcessor('131018-1Al')

see.getDataFromGNode()
# ipdb.set_trace()
see.downSampleVibSignal()
# ipdb.set_trace()
see.getStimulusEpochs()
# ipdb.set_trace()
see.extractResponse()
# ipdb.set_trace()
plt.figure();plt.show(block=False)
for respInd in range(len(see.responseVTraces)):
    plt.cla()
    see.getSegment(respInd)
    plt.draw()
    ch = 'n'
    ch = raw_input('Next(n)/Quit(q):')
    if ch == 'q':
        break
