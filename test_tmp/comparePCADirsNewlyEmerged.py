from GJEMS.morph.morph import getPCADetails
import os
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

def add3Vecs3D(ax, points, colour, scale=1):

    assert len(points) == 3
    markers = ['s', 'o', '^']
    for pointInd, point in enumerate(points):
        ax.plot([0, scale * point[0]], [0, scale * point[1]], [0, scale * point[2]],
                color=colour, marker=markers[pointInd])
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.draw()
    plt.draw()

newlyEmergedSWCPath = 'swcFiles/GoodSamplesDLInt1_v2/newlyEmerged'

newlyEmergedNrns = ['HB130523-3NS_3ptSoma_USTD.swc',
                    'HB130605-1NS_3ptSoma_USTD.swc',
                    'HB130605-2NS_3ptSoma_USTD.swc'
]
cols = ['r', 'g', 'b', 'm', 'k', 'c', 'r', 'g']

newlyEmergedSWCs = [os.path.join(newlyEmergedSWCPath, x) for x in newlyEmergedNrns]

fig = plt.figure()
plt.show(block=False)
ax = fig.add_subplot(111, projection='3d')

for swcInd, swc in enumerate(newlyEmergedSWCs):

    evecs, std = getPCADetails(swc, center=False)
    add3Vecs3D(ax, evecs.T, cols[swcInd])

plt.draw()

