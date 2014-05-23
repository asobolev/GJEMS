from LMIO.wrapper import *
import matplotlib.pyplot as plt
import os
import numpy as np

# SWCPath = 'swcFiles/GoodSamplesDLInt1_v2/forager'
#
# swcFNames = [
#                 'HB130313-4NS_3ptSoma_FSTD.swc',
#                 'HB130322-1NS_3ptSoma_FSTD.swc',
#                 'HB130408-1NS_3ptSoma_FSTD.swc',
#                 'HB130425-1NS_3ptSoma_FSTD.swc',
#                 'HB130501-2NS_3ptSoma_FSTD.swc'
#                 ]

SWCPath = 'swcFiles/GoodSamplesDLInt1_v2/newlyEmerged'

swcFNames = [
                    'HB130523-3NS_3ptSoma_FSTD.swc',
                    'HB130605-1NS_3ptSoma_FSTD.swc',
                    # 'HB130605-2NS_3ptSoma_USTD.swc'
]

swcFiles = [os.path.join(SWCPath, x) for x in swcFNames]

# swcFiles.append('swcFiles/HB060602_3ptSoma.swc')

LMOutput = getMeasure(['EucDistance'], swcFiles)


print LMOutput[0]['WholeCellMeasures'][:, 4:]