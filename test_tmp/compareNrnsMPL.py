import numpy as np
from GJEMS.morph.morph import plotPoints3D, addPoints3D


swc1 = '/home/ajay/PowerFolders/GinJangNDB_Upload/SigenSegmentations/Results/GoodSamplesDLInt1/forager/' \
       + 'HB130322-1NS_STD.swc'

swc2 = '/home/ajay/PowerFolders/GinJangNDB_Upload/SigenSegmentations/Results/GoodSamplesDLInt1/forager/' \
       + 'HB130425-1NS_STD.swc'

swcData1 = np.loadtxt(swc1)
swcData2 = np.loadtxt(swc2)

ax = plotPoints3D(swcData1[:, 2:5], 'rx')
addPoints3D(ax, swcData2[:, 2:5], 'bx')
