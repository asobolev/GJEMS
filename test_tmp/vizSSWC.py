import sys
sys.path.append('/home/ajay/repos/GJEMS/GJEMS/morph')

from blenderHelper import BlenderSWCImporter
import numpy as np

print(sys.argv)
assert len(sys.argv) == 5, \
    'This script takes only 5 arguments, with the path of the swcfile expected as the 5th arguement, but ' \
    + str(len(sys.argv)) + ' found'
sswcFName = sys.argv[4]


cols = np.asarray(      [[ 0.        ,  0.        ,  0.5       ],
                        [ 0.        ,  0.00196078,  1.        ],
                        [ 0.        ,  0.50392157,  1.        ],
                        [ 0.08538899,  1.        ,  0.88235294],
                        [ 0.49019608,  1.        ,  0.47754586],
                        [ 0.89500316,  1.        ,  0.07273877],
                        [ 1.        ,  0.58169935,  0.        ],
                        [ 1.        ,  0.11692084,  0.        ]])






blenderObj = BlenderSWCImporter(sswcFName, colMap=cols, matchRootOrigin=False)
blenderObj.importWholeSWC()