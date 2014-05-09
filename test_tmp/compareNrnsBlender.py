import sys
sys.path.append('/home/ajay/repos/GJEMS/GJEMS/morph')

from blenderHelper import BlenderSWCImporter


# swc1 = '/home/ajay/PowerFolders/GinJangNDB_Upload/SigenSegmentations/Results/GoodSamplesDLInt1/forager/' \
#        + 'HB130501-2NS_STD.swc'
#
# swc2 = '/home/ajay/PowerFolders/GinJangNDB_Upload/SigenSegmentations/Results/GoodSamplesDLInt1/forager/' \
#        + 'HB130313-4NS_3ptSoma_STD.swc'
#
# swc2 = '/home/ajay/PowerFolders/GinJangNDB_Upload/SigenSegmentations/Results/GoodSamplesDLInt1/newlyEmerged/' \
#        + 'HB130523-3NS_STD.swc'

# swc1 = '/home/ajay/PowerFolders/GinJangNDB_Upload/SigenSegmentations/Results/GoodSamplesDLInt1_v2/forager/' \
#        + 'HB130313-4NS_3ptSoma_STD.swc'

#swc1 = '/home/ajay/PowerFolders/GinJangNDB_Upload/SigenSegmentations/Results/GoodSamplesDLInt1_v2/forager/' \
       #+ 'HB130425-1NS_3ptSoma_STD.swc'

# swc1 = 'swcFiles/GoodSamplesDLInt1_v2/forager/' \
#        + 'HB130408-1HNS_3ptSoma_STD.swc'

# swc1 = 'swcFiles/GoodSamplesDLInt1_v2/forager/' \
#        + 'HB130501-2NS_3ptSoma_STD.swc'


# swc1 = 'swcFiles/GoodSamplesDLInt1_v2/forager/' \
#        + 'HB130408-1NS_3ptSoma_STD.swc'

swc1 = 'swcFiles/GoodSamplesDLInt1_v2/newlyEmerged/' \
       + 'HB130605-1NS/HB130605-1NS_3ptSoma_STD.swc'

swc2 = 'swcFiles/GoodSamplesDLInt1_v2/forager/' \
       + 'HB130313-4NS_3ptSoma_STD.swc'

# swc2 = 'swcFiles/GoodSamplesDLInt1_v2/forager/' \
#        + 'HB130425-1NS_3ptSoma_STD.swc'

# swc1 = 'swcFiles/HB060602_3ptSoma_STD.swc'

# nrnBlender1 = BlenderSWCImporter(swc1, matchRootOrigin=True)
# nrnBlender2 = BlenderSWCImporter(swc2, add=True, matchRootOrigin=True)



nrnBlender1 = BlenderSWCImporter(swc1, matchRootOrigin=False)
nrnBlender2 = BlenderSWCImporter(swc2, add=True, matchRootOrigin=False)


nrnBlender1.importSWC([1, 0, 0])
nrnBlender2.importSWC([0, 1, 0])