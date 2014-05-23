import sys
sys.path.append('/home/ajay/repos/GJEMS/GJEMS/morph')

from blenderHelper import BlenderSWCImporter





swcs = [
    # 'swcFiles/GoodSamplesDLInt1_v2/forager/HB130408-1NS_3ptSoma_FSTD.swc',
    # 'swcFiles/GoodSamplesDLInt1_v2/forager/HB130501-2NS_3ptSoma_FSTD.swc',
    # 'swcFiles/GoodSamplesDLInt1_v2/forager/HB130313-4NS_3ptSoma_FSTD.swc',
    # 'swcFiles/GoodSamplesDLInt1_v2/forager/HB130322-1NS_3ptSoma_USTD.swc',
    # 'swcFiles/GoodSamplesDLInt1_v2/forager/HB130425-1NS_3ptSoma_USTD.swc',

    'swcFiles/GoodSamplesDLInt1_v2/forager/HB130322-1NS_3ptSoma_FSTD_TipColoured.sswc',
    'swcFiles/GoodSamplesDLInt1_v2/forager/HB130313-4NS_3ptSoma_FSTD_TipColoured.sswc',
    'swcFiles/GoodSamplesDLInt1_v2/forager/HB130501-2NS_3ptSoma_FSTD_TipColoured.sswc',

    # 'swcFiles/GoodSamplesDLInt1_v2/newlyEmerged/HB130523-3NS_3ptSoma_USTD.swc',
    # 'swcFiles/GoodSamplesDLInt1_v2/newlyEmerged/HB130605-1NS_3ptSoma_USTD.swc',
    # 'swcFiles/GoodSamplesDLInt1_v2/newlyEmerged/HB130605-2NS_3ptSoma_USTD.swc',

    # 'swcFiles/GoodSamplesDLInt1_v2/newlyEmerged/HB130523-3NS_3ptSoma.swc',
    # 'swcFiles/GoodSamplesDLInt1_v2/newlyEmerged/HB130605-1NS_3ptSoma.swc',

]


cols = [[ 0.        ,  0.        ,  0.5       ],
        [ 0.        ,  0.00196078,  1.        ],
        [ 0.        ,  0.50392157,  1.        ],
        [ 0.08538899,  1.        ,  0.88235294],
        [ 0.49019608,  1.        ,  0.47754586],
        [ 0.89500316,  1.        ,  0.07273877],
        [ 1.        ,  0.58169935,  0.        ],
        [ 1.        ,  0.11692084,  0.        ]]

nrnsBlender = []
matchOrigin = False


for nrnInd, nrn in enumerate(swcs):

    if nrnInd == 0:
        add = False
    else:
        add = True

    tmpB = BlenderSWCImporter(nrn, add, matchOrigin, colMap=cols)

    # tmpB.importSWC(cols[nrnInd])

    tmpB.importWholeSWC()

    nrnsBlender.append(tmpB)



