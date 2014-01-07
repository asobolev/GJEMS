import time
from easygui import fileopenbox

smr = fileopenbox('Indicate the smr file to use', filetypes=['*.smr'])

t = []
t.append(time.clock())
testEphys = RawDataUploader(smr, 'spike2Files/Neuron_Database.csv')
# testEphys.plotVibEpoch([0, 20])
t.append(time.clock())
testEphys.parseSpike2Data()
t.append(time.clock())
testEphys.extractCSVMetaData()
t.append(time.clock())
testEphys.uploadToGNode()
t.append(time.clock())
print t
# plt.figure();plt.show(block=False)
# for seg in testEphys.extractedBlock.segments[::10]:
#
#     plt.cla()
#     resp = seg.analogsignals[0]
#     stim = seg.analogsignals[1]
#
#     plt.plot(range(len(resp)) * resp.sampling_period + resp.t_start, resp, 'r')
#     plt.plot(range(len(stim)) * stim.sampling_period + stim.t_start, stim, 'b')
#     plt.draw()
#     ch = 'c'
#     ch = raw_input('Continue(c)/quit(q):')
#     if ch == 'q':
#         break

# testEphys.showPlot()
# plt.show(block=False)
testEphys.cleanup()