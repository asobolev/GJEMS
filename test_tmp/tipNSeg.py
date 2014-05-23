from GJEMS.morph.morph import BasicMorph
import os
from matplotlib import pyplot as plt
import numpy as np
import neuron as nrn

foragerSWCPath = 'swcFiles/GoodSamplesDLInt1_v2/forager'

foragerSWCFNames = [
    'HB130313-4NS_3ptSoma_FSTD.swc',
    # 'HB130322-1NS_3ptSoma_FSTD.swc',
    # 'HB130408-1NS_3ptSoma_FSTD.swc',
    # 'HB130425-1NS_3ptSoma_FSTD.swc',
    # 'HB130501-2NS_3ptSoma_FSTD.swc'
]

foragerSWCFiles = [os.path.join(foragerSWCPath, x) for x in foragerSWCFNames]

# neSWCPath = 'swcFiles/GoodSamplesDLInt1_v2/newlyEmerged'
#
# neSWCFNames = [
#     'HB130523-3NS_3ptSoma_FSTD.swc',
#     'HB130605-1NS_3ptSoma_FSTD.swc',
#     'HB130605-2NS_3ptSoma_USTD.swc'
# ]

# neSWCFiles = [os.path.join(neSWCPath, x) for x in neSWCFNames]

swcFile = foragerSWCFiles[0]

# fig = plt.figure()
# plt.show(block=False)

NRN = BasicMorph(swcFile)


# NRN.initDistances()
tipNSegs = [x.sec.nseg for x in NRN.tipPtrs.values()]
hist, bins = np.histogram(tipNSegs, np.arange(10) + 0.5)
print hist/float(sum(hist)), bins

