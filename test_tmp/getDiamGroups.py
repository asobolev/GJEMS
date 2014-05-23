import matplotlib.pyplot as plt
import os
import numpy as np
from scipy.stats import norm


diamStep = 0.05
swcDiamsList = []

foragerSWCPath = 'swcFiles/GoodSamplesDLInt1_v2/forager'

foragerSWCFNames = [
    'HB130313-4NS_3ptSoma_FSTD.swc',
    'HB130322-1NS_3ptSoma_FSTD.swc',
    'HB130408-1NS_3ptSoma_FSTD.swc',
    'HB130425-1NS_3ptSoma_FSTD.swc',
    'HB130501-2NS_3ptSoma_FSTD.swc'
]

foragerSWCFiles = [os.path.join(foragerSWCPath, x) for x in foragerSWCFNames]

neSWCPath = 'swcFiles/GoodSamplesDLInt1_v2/newlyEmerged'

neSWCFNames = [
    'HB130523-3NS_3ptSoma_FSTD.swc',
    'HB130605-1NS_3ptSoma_FSTD.swc',
    'HB130605-2NS_3ptSoma_USTD.swc'
]

neSWCFiles = [os.path.join(neSWCPath, x) for x in neSWCFNames]

fig1 = fig = plt.figure()
plt.show(block=False)

# cols = ['r', 'g', 'b', 'm', 'k', 'c']

cols = ['b'] * len(foragerSWCFiles)


for swcFile, col in zip(foragerSWCFiles, cols):

    swcDiams = np.loadtxt(swcFile)[:, 5]
    swcDiamsList.append(swcDiams)
    bins = np.arange(0, max(swcDiams), diamStep)
    hist, binEdges = np.histogram(swcDiams, bins)
    normHist = hist/ float(sum(hist))
    plt.plot(binEdges[:-1], normHist, color = col, marker = 'o')
    print swcFile
    print max(normHist)

cols = ['r'] * len(neSWCFiles)

for swcFile, col in zip(neSWCFiles, cols):

    swcDiams = np.loadtxt(swcFile)[:, 5]
    swcDiamsList.append(swcDiams)
    bins = np.arange(0, max(swcDiams), diamStep)
    hist, binEdges = np.histogram(swcDiams, bins)
    normHist = hist/ float(sum(hist))
    plt.plot(binEdges[:-1], normHist, color = col, marker = 'o')
    print swcFile
    print max(normHist)

plt.draw()



# diams = np.hstack(swcDiamsList)
#
# minDiam = min(diams)
# maxDiam = max(diams)
#
#
# bins = np.arange(minDiam, maxDiam, diamStep)
# hist, binEdges = np.histogram(diams, bins)
#
#
# fig = plt.figure()
# plt.show(block=False)
#
# plt.plot(binEdges[:-1], hist, 'r-*')
# distMax = np.max(hist)
# gaussFit = norm(binEdges[np.argmax(hist)], diams.std())
# plt.plot(binEdges, distMax * gaussFit.pdf(binEdges) / gaussFit.pdf(gaussFit.mean()), 'bx-')
# plt.draw()
