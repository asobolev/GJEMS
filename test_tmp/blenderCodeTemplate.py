#Author: Ajayrama Kumaraswamy(ajayramak@bio.lmu.de)
#Date: 3 March 2014
#Place: Dept. of Biology II, LMU, Munich


#********************************************List of Dependencies*******************************************************
#The following code has been tested with the indicated versions on 64bit Linux and PYTHON 2.7.3
#blender: 2.6.9

#***********************************************************************************************************************

import bpy
from mathutils import Vector, Matrix
from math import pi as PI
from math import cos, sin, acos
import os


class BlenderSWCImporter:

    #*******************************************************************************************************************
    def readSWC(self):
        """
        Read the data of all points in the swc file.
        :return:
        """

        swcPointData = {}
        with open(self.swcFName, 'r') as fle:
            line = fle.readline()
            while not line == '':

                if not line[0] == '#':
                    entries = line.split(' ')
                    swcPointData[float(entries[0])] = [float(x) for x in entries[2:7]]

                line = fle.readline()

        return swcPointData

    #*******************************************************************************************************************

    def __init__(self, swcFName, add=False, matchRootOrigin=True, swcData=None):

        if not add == True:
            #Remove the default objects in the blender scene.
            bpy.ops.object.select_all(action='TOGGLE')
            bpy.ops.object.select_all(action='TOGGLE')
            bpy.ops.object.delete()


        self.swcFName = swcFName
        self.swcName = os.path.split(swcFName)[1].rstrip('.swc')

        if swcData is None:

            self.swcPointData = self.readSWC()

        else:

            self.swcPointData = swcData


        self.nCirclePoints = 16
        assert self.nCirclePoints % 2 == 0, 'No of points on the circle circumference has to be even'

        if matchRootOrigin:
            self.originPoint = Vector(self.swcPointData[1][:3])
        else:
            self.originPoint = Vector([0, 0, 0])
        self.scaleDownBy = float(100)

        self.swcPointDone = [False] * len(self.swcPointData)
        self.blenderCircleIndsPerSWCPoint = [[] for x in range(len(self.swcPointData))]

        #For these, each entry corresponds to one set of circle added to blender.

        self.vertIndexStartsPerPoint = []
        self.normals = []
        self.refVecsInPlane = []

        self.verts = []
        self.faces = []
        self.nBlenderCircles = 0

    #*******************************************************************************************************************

    def getFaceIndices(self, vertsOfVec1Start, vertsOfVec2Start):
        """
        It is assumed that self.nCirclePoints contains of a list of integer indices. Also, it is assumed that the set of points belonging to a circle are contiguous in this list. Given the starting points of the two sets of vertex indices belonging to two circles, returns a list of quadruplets, each quadruplet representing a quadrilateral face forming the surface joining the two circles.
        :param vertsOfVec1Start: interger, start index in self.nCirlePoints of the set of vertices belonging to the first circle.
        :param vertsOfVec2Start: interger, start index in self.nCirlePoints of the set of vertices belonging to the second circle.
        :return:a list of quadruplets, each quadruplet representing a quadrilateral face forming the surface joining the two circles.
        """



        return [(vertsOfVec1Start + x,
                 vertsOfVec1Start + ((x + 1) % self.nCirclePoints),
                 vertsOfVec2Start + ((x + 1) % self.nCirclePoints),
                 vertsOfVec2Start + x) for x in range(self.nCirclePoints)]

    #*******************************************************************************************************************

    def getNormDiffVector(self, vector1, vector2):
        """
        Returns the normalized difference of vector1 and vector2
        :param vector1: mathutils.Vector object of Blender
        :param vector2: mathutils.Vector object of Blender
        :return:normalized difference of vector1 and vector2
        """

        diffVector = vector1 - vector2
        diffVector.normalize()
        return diffVector

    #*******************************************************************************************************************

    def getCircleVerts(self, pointVec, pointNormal, pointDiam, refVec=None):
        """
        Given point, a normal and a diameter, generates self.nCirclePoints number of points on the circle defined by the input. If the 'refVec' vector is given, the first point (of the list of points returned) will be the projection of the tip of refVec moved to pointVec onto the plane perpendicular to pointNormal.
        :param pointVec: mathutils.Vector object of Blender
        :param pointNormal: mathutils.Vector object of Blender
        :param pointDiam: integer
        :param refVec: mathutils.Vector object of Blender
        :return: circlePoints, refVecInPlane
        circlePoints: list of length self.nCirclePoints. Each element is a mathutils.Vector objects of Blender
        refVecInPlane: first point in the above list - pointVec
        """

        #rotation matrix for rotating b to a: Matrix.Rotation(b.angle(a), dimension, b.cross(a))
        #here pointNormal is 'a', (0,0,1) is 'b'

        rotationMatrix = Matrix.Rotation(acos(pointNormal.z), 3, Vector([-pointNormal.y, pointNormal.x, 0]))

        # the points of the circle are first constructed assuming the pointNormal is (0,0,1). Let this frame of
        # reference be call Ref1

        thetaAdditional = 0

        if refVec is not None:

            #shift and rotate refVec to bring it to Ref1
            refVec.normalize()
            refVecShifted = refVec
            newRefVec = rotationMatrix.inverted() * refVecShifted

            #nearest point on the r=1 circle is the projection of newRefVec on XY plane(just set z=0)
            #thetaAdditional is just angle between newRefVec with (1,0,0)

            newRefVec.z = 0
            newRefVec.normalize()

            thetaAdditional = acos(newRefVec.x)

        #Using cylindrical coordinates r, theta and z

        r = pointDiam

        thetaInterval = 2 * PI / self.nCirclePoints
        thetas = [x * thetaInterval for x in range(self.nCirclePoints)]

        circlePointsRotated = [Vector([r * cos(theta + thetaAdditional), r * sin(theta + thetaAdditional), 0])
                               for theta in thetas]

        circlePoints = [pointVec + rotationMatrix * x for x in circlePointsRotated]

        return circlePoints, circlePoints[0] - pointVec

    #*******************************************************************************************************************

    def addVertices(self, verts, normal, refVecInPlane, swcPointInd):
        """
        Adds all the inputs to corresponding collections defined in __init__. Increments self.nBlenderPoints and marks the point done in self.swcPointDone
        :param verts: list of length self.nCirclePoints. Each element is a mathutils.Vector objects of Blender
        :param normal: mathutils.Vector object of Blender
        :param refVecInPlane: mathutils.Vector object of Blender
        :param swcPointInd: integer, index of the point in the swcfile(col 1)
        :return:
        """

        self.swcPointDone[swcPointInd - 1] = True
        self.vertIndexStartsPerPoint.append(self.nBlenderCircles * self.nCirclePoints)
        self.blenderCircleIndsPerSWCPoint[swcPointInd - 1].append(self.nBlenderCircles)
        self.verts.extend(verts)
        self.normals.append(normal)
        self.refVecsInPlane.append(refVecInPlane)
        self.nBlenderCircles += 1

    #*******************************************************************************************************************

    def correctNumbering(self, verts):
        """
        Returns verts[0,-1, -2,.....,2,1]
        :param verts: list
        :return:
        """

        allButFirst = verts[1:]
        allButFirst.reverse()
        correctedVerts = [verts[0]]
        correctedVerts.extend(allButFirst)
        return correctedVerts

    #*******************************************************************************************************************

    def addNewSection(self, pointVec, pointDiam, rootVec, rootDiam, pointInd, rootInd):
        """
        Adds equally spaced points along the circumference of the two circles around pointVec and rootVec with diameters pointDiam and rootDiam, respectively, to self.verts. Defines faces using self.getFaceIndices() and add to self.faces.
        :param pointVec: mathutils.Vector object of Blender
        :param pointDiam: integer
        :param rootVec: mathutils.Vector object of Blender
        :param rootDiam: integer
        :param pointInd: integer, index of the point in the swcfile(col 1)
        :param rootInd: integer, index of the root of the point in the swcfile(col 7)
        :return:
        """

        rootNormal = self.getNormDiffVector(pointVec, rootVec)

        vertsOfRoot, refVecIPRoot = self.getCircleVerts(rootVec, rootNormal, rootDiam)

        self.addVertices(vertsOfRoot, rootNormal, refVecIPRoot, rootInd)

        pointNormal = self.getNormDiffVector(rootVec, pointVec)

        vertsOfPoint, refVecIPPoint = self.getCircleVerts(pointVec, rootNormal, pointDiam,
                                                          self.refVecsInPlane[-1])

        #because the normals are antiparallel, the direction of numbering the points would be opposite. Correcting.

        self.addVertices(vertsOfPoint, pointNormal, refVecIPPoint, pointInd)

        secFaces = self.getFaceIndices(self.vertIndexStartsPerPoint[-2], self.vertIndexStartsPerPoint[-1])
        self.faces.extend(secFaces)

    #*******************************************************************************************************************

    def addPointsAndFaces(self, pointVec, pointDiam, pointNormal, indexOfRootPoint, refVecIP, pointInd):
        """
        Adds self.nCirclePoints number of points for the given pointVec, pointDiam and pointNormal. These point are equally spaced along the circumference of the circle at pointVec, with diameter pointDiam and in the plane perpendicular to pointNormal. Adds to self.faces, the faces between the points just defined and the points on the circle around a point whose index in the swc file(col 1) is indexOfRootPoint. Read documentation of getCircleVerts() for more of refVecIP.
        :param pointVec: mathutils.Vector object of Blender
        :param pointDiam: integer
        :param pointNormal:mathutils.Vector object of Blender
        :param indexOfRootPoint: integer
        :param refVecIP: mathutils.Vector object of Blender
        :param pointInd: integer
        :return:
        """

        vertsOfPoint, refVecIP = self.getCircleVerts(pointVec, pointNormal,
                                                     pointDiam, refVecIP)
        self.addVertices(vertsOfPoint, pointNormal, refVecIP, pointInd)

        secFaces = self.getFaceIndices(self.vertIndexStartsPerPoint[indexOfRootPoint], self.vertIndexStartsPerPoint[-1])
        self.faces.extend(secFaces)

    #*******************************************************************************************************************

    def addSection(self, pointInd):

        """
         Adds to self.verts, equally spaced points along the circumferences of the two circles, one around the point with index pointInd in the swc file(col 1) and one around it's root. Add to self.faces, faces forming the surface between these two circles using getFaceIndices.
        :param pointInd: integer
        :return:
        """

        minAngle = lambda vec1, vec2: min(vec1.angle(vec2), vec1.angle(-vec2))

        pointData = self.swcPointData[pointInd]
        pointVec = (Vector(pointData[:3]) - self.originPoint) / self.scaleDownBy
        pointDiam = pointData[3] / self.scaleDownBy

        rootInd = int(pointData[4])
        rootData = self.swcPointData[rootInd]
        rootVec = (Vector(rootData[:3]) - self.originPoint) / self.scaleDownBy
        rootDiam = rootData[3] / self.scaleDownBy

        if pointVec == rootVec:
            print('Warning: Points at line ' + str(pointInd) + 'and line ' + str(rootInd) +
                  'have the same XYZ Coordinates in file ' + self.swcName)

        else:

        #***************************************************************************************************************

        # This line can replace all the code below so that for each section, two new circles are added.
        #   self.addNewSection(pointVec, pointDiam, rootVec, rootDiam, pointInd, rootInd)

        #***************************************************************************************************************

            #if both the point and root have not been added
            if not self.swcPointDone[rootInd]:

                self.addNewSection(pointVec, pointDiam, rootVec, rootDiam, pointInd, rootInd)

            #if the root point has already been added
            else:
                rootPointIndices = self.blenderCircleIndsPerSWCPoint[rootInd - 1]
                pointNormal = self.getNormDiffVector(rootVec, pointVec)

                anglesWithRootNormals = [minAngle(pointNormal, self.normals[x]) for x in rootPointIndices]
                minAngle = min(anglesWithRootNormals)
                if minAngle > (PI / 4.0):

                    self.addNewSection(pointVec, pointDiam, rootVec, rootDiam, pointInd, rootInd)

                else:

                    indexOfRootPointToUse = rootPointIndices[anglesWithRootNormals.index(minAngle)]

                    #if the closest vector(by angle) was antiparallel to the actual normal vector, invert the stored refVecInPlane
                    if pointNormal.angle(self.normals[indexOfRootPointToUse]) < (PI / 4.0):
                        refVecIP = self.refVecsInPlane[indexOfRootPointToUse]
                    else:
                        refVecIP = -self.refVecsInPlane[indexOfRootPointToUse]

                    self.addPointsAndFaces(pointVec, pointDiam, pointNormal, indexOfRootPointToUse, refVecIP, pointInd)

    #*******************************************************************************************************************

    def definePoints(self):
        """
        For each point of the swc file which is not the root, adds the circles and faces that define the 3D frustrum representing the section.
        :return:
        """

        for pointInd in self.swcPointData.keys():

            pointInd = int(pointInd)
            if not self.swcPointData[pointInd][-1] == -1:
                self.addSection(pointInd)

    #*******************************************************************************************************************



    def drawInBlender(self, col):
        """
        Uses the defined points in self.verts and faces in self.faces to construct a 3D object in Blender
        :return:
        """
        mesh = bpy.data.meshes.new(self.swcName)
        nrn = bpy.data.objects.new(self.swcName, mesh)
        bpy.context.scene.objects.link(nrn)

        mat = bpy.data.materials.new(self.swcName)
        mat.diffuse_color = col
        nrn.active_material = mat

        mesh.from_pydata(self.verts, [], self.faces)
        mesh.update(calc_edges=True)

    #*******************************************************************************************************************

    def export2Obj(self, fileName, col=[1, 0, 0]):
        """
        This function generates an OBJ file taking the swcfile path.
        :param fileName: Absolute path of swc file.
        :return:
        """

        self.definePoints()
        self.drawInBlender(col)
        bpy.ops.export_scene.obj(filepath=fileName)
        #*******************************************************************************************************************

    def importSWC(self, col=[1, 0, 0]):
        """
        This function imports the neuron in swcfile.
        :param fileName: Absolute path of swc file.
        :param col: RGB triplet defining the color of the neuron
        :return:
        """

        self.definePoints()
        self.drawInBlender(col)
        #*******************************************************************************************************************
        #To add color
        #
        #mat = bpy.data.materials.new("dorsalBranch")
        #mat.diffuse_color = (r,g,b)
        #object.active_material = mat

