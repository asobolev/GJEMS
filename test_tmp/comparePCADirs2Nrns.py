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

# swc1 = 'swcFiles/GoodSamplesDLInt1_v2/forager/' \
#        + 'HB130425-1NS_3ptSoma_STD.swc'

swc1 = 'swcFiles/GoodSamplesDLInt1_v2/forager/' \
       + 'HB130313-4NS_3ptSoma_STD.swc'

swc2 = 'swcFiles/GoodSamplesDLInt1_v2/forager/' \
       + 'HB130322-1NS_3ptSoma_STD.swc'

# swc2 = 'swcFiles/HB060602_3ptSoma_STD.swc'

evec1, stds = getPCADetails(swc1, center=False)
evec2, stds = getPCADetails(swc2, center=False)


fig = plt.figure()
plt.show(block=False)
ax = fig.add_subplot(111, projection='3d')

add3Vecs3D(ax, evec1.T, 'r')
add3Vecs3D(ax, evec2.T, 'g')


