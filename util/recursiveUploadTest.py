import neo
import odml
from gnodeclient import *
import numpy as np
import quantities as qu
import time
# from GJMorphSim.ephys.GNodeUpoadHelpers import *
import ipdb

ss = session.create(location="http://predata.g-node.org", username="bob", password="pass")
blk = neo.Block(name='testBlock1')
for ind1 in range(3):

    seg = neo.Segment(name='testSegment' + str(ind1), index=ind1)
    seg.block = blk

    for ind2 in range(3):
        sp = neo.SpikeTrain(name='SpikeTrain' + str(ind2), times=np.random.rand(10) * qu.s, t_stop=1.2)
        sp.segment = seg
        seg.spiketrains.append(sp)

    for ind2 in range(3):
        sp = neo.Spike(name='Spike' + str(ind2), time=np.random.rand() * qu.s)
        sp.segment = seg
        seg.spikes.append(sp)

    for ind2 in range(3):
        irr = neo.IrregularlySampledSignal(name='IrregularlySampled' + str(ind2), times=np.random.rand(10) * qu.s,
                                           signal=np.random.rand(10) * qu.mV)
        irr.segment = seg
        seg.irregularlysampledsignals.append(irr)

    for ind2 in range(3):
        an = neo.AnalogSignal(name='AnalogSignal' + str(ind2), signal=np.random.rand(10) * qu.mV,
                              sampling_rate=10 * qu.Hz)
        an.segment = seg
        seg.analogsignals.append(an)

    for ind2 in range(3):
        an = neo.AnalogSignalArray(name='AnalogSignalArray' + str(ind2), signal=np.random.rand(10, 10) * qu.mV,
                                   sampling_rate=10 * qu.Hz)
        sp.segment = seg
        seg.analogsignalarrays.append(an)

    for ind2 in range(3):
        ev = neo.Event(name='Event' + str(ind2), time=np.random.rand() * qu.s, label='h')
        ev.segment = seg
        seg.events.append(ev)

    for ind2 in range(3):
        eva = neo.EventArray(name='EventArray' + str(ind2), times=np.random.rand(10) * qu.s, label=['h'] * 10)
        eva.segment = seg
        seg.eventarrays.append(eva)

    for ind2 in range(3):
        ep = neo.Epoch(name='Epoch' + str(ind2), time=np.random.rand() * qu.s, duration=np.random.rand() * qu.s,
                       label='cc')
        ep.segment = seg
        seg.epochs.append(ep)

    for ind2 in range(3):
        epa = neo.EpochArray(name='EpochArray' + str(ind2), times=np.random.rand(10) * qu.s,
                             durations=np.random.rand(10) * qu.s, labels=['cc'] * 10)
        epa.segment = seg
        seg.epocharrays.append(epa)

    blk.segments.append(seg)


mainSec = Native.SECTION(name='testSection', type='experiment')
subSec = Native.SECTION(name='testSubSection', type='experiment/electrophysiology')
for ind in range(3):
    p = odml.Property(name='Prop' + str(ind), value=np.random.rand(5).tolist())
    subSec.append(p)

mainSec.append(subSec)

for se in mainSec.sections:
    if se.name == 'testSubSection':
        blk.section = se
        se.blocks.append(blk)
        break

print 'Uploading metadata ' + str(time.clock())
exceptionsSec = ss.set_all(mainSec)
print 'Uploading metadata Done ' + str(time.clock())


# blkLoc = uploadNewBlockRecursive(ss, blk)
# secLoc = uploadNewSectionRecursive(ss, mainSec)

# blck = ss.get(blkLoc)
# sc = ss.get(secLoc)
# blck.section = sc
# blck = ss.set(blck)




# print 'Uploading Connection ' + str(time.clock())
# exceptionsBlk = ss.set_all(blk)
# print 'Uploading Connection Done ' + str(time.clock())


ch = 'n'
ch = raw_input('Delete Objects Created(This is a point where one could check if the uploaded objects are as expected on the website)?<y/n>')
if ch == 'y':
    if checkIfExistsBlock(ss, blk.name):
        deleteExistentBlock(ss, blk.name)

    if checkIfExistsSection(ss, mainSec.name):
        deleteExistentSection(ss, mainSec.name)

