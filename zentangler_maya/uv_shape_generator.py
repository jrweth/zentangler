import pymel.core as pm
from pymel.all import mel
from zentangler.shape import Shape
from shapely.geometry import MultiPolygon, Polygon


class UVShapeGenerator:
    """
    Class which handles the creation of a shape from the border edges of a UV map
    """

    def __init__(self, object):
        """
        initialize the generator with the test_maya.general.PyNode object which contains the geometry

        Parameters:
            object: test_maya.core.general.PyNode
        """
        self.obj = object

    def get_current_uv_shell_shapes(self):
        polygons = []
        pm.select(self.obj.name())
        uv_f = self.obj.getAssignedUVs()
        uv_face_num_points = uv_f[0]
        uv_face_points = uv_f[1]
        uv_s= self.obj.getUvShellsIds()
        uv_shell_ids = uv_s[0]
        num_uv_shells = uv_s[1]
        uv_coords = self.obj.getUVs()

        uv_shell_face_polys = []
        # create the list of faces
        for i in range(num_uv_shells):
            uv_shell_face_polys.append([])

        face_index = 0
        # loop through the uv faces
        for num_face_verts in uv_face_num_points:
            # for each face gather the points of all the uvs
            points = []
            # get the uvs making up each uv face
            for i in range(num_face_verts):
                uv_index = uv_face_points[face_index]
                shell_id = uv_shell_ids[uv_index]
                points.append((uv_coords[0][uv_index], uv_coords[1][uv_index]))
                face_index += 1
            uv_shell_face_polys[shell_id].append(Polygon(points))

        # now that we have a list of polygons for each uv_shell lets combine them all together
        shapes_list = []
        for shell_id in range(num_uv_shells):
            combined = uv_shell_face_polys[shell_id][0]
            for poly_index in range(1, len(uv_shell_face_polys[shell_id])):
                combined = combined.union(uv_shell_face_polys[shell_id][poly_index])

            #now that we have our combined polygon let's make a shape
            if isinstance(combined, Polygon):
                shapes_list.append([Shape(geometry=MultiPolygon([combined]))])
            elif isinstance(combined, MultiPolygon):
                shapes_list.append([Shape(geometry=combined)])
            else:
                print ("neither polygon or multipolygon")


        #now we return our array of shell shapes
        return shapes_list



    def get_current_uv_shape(self):
        """
        use shapely to combine all the uv polygons into 1 uv polygon
        """

        # get all of the uv polygons from each face
        polygons = []
        for face in self.obj.f:
            uvs = face.getUVs()
            points = []

            for i in range(len(uvs[0])):
                points.append((uvs[0][i], uvs[1][i]))
            polygons.append(Polygon(points, []))

        #use shapely to combine the uv polygons
        combined = polygons[0]
        for i in range(1, len(polygons)):
            combined = combined.union(polygons[i])


        if isinstance(combined, Polygon):
            return Shape(geometry=MultiPolygon([combined]))

        return Shape(geometry=combined)

    def get_silhouette_shape(self):
        object_name = self.obj.name()
        map_name = "zentanglerMap"

        # if the zentanglerMap UV map does not yet exist, create it
        indices = pm.polyUVSet(object_name, query=True, allUVSetsIndices=True)
        already_created = False
        for i in indices[:]:
            name = pm.getAttr(object_name + ".uvSet[" + str(i) + "].uvSetName")
            if name == map_name:
                already_created = True
                break

        if not already_created:
            pm.polyUVSet(create=True, uvSet=map_name)

        # select all faces and do the poly projection
        pm.polyUVSet(currentUVSet=True, uvSet=map_name)
        all_faces = object_name + ".f[0:" + str(self.obj.numFaces() - 1) + "]"

        # perform the UV projection from the camera view
        pm.polyProjection(all_faces, type='Planar', md='p')
        pm.select(self.obj)

        # select just the front facing faces
        mel.eval('buildObjectMenuItemsNow "MainPane|viewPanes|modelPanel4|modelPanel4|modelPanel4|modelPanel4ObjectPop"')
        mel.eval('doMenuComponentSelectionExt("' + object_name + '", "facet", 1);')
        mel.eval("selectUVFaceOrientationComponents {} 0 1 1;")

        #loop through the faces and get the UV points for each UV face
        faces = pm.ls(selection=True, flatten=True)
        polygons = []
        for face in faces:
            uvs = face.getUVs(uvSet=map_name)
            points = []

            for i in range(len(uvs[0])):
                # point = (uvs[0][i], uvs[1][i])
                points.append((uvs[0][i], uvs[1][i]))
            polygons.append(Polygon(points, []))

        # use shapely to combine the uv polygons
        combined = polygons[0]
        for i in range(1, len(polygons)):
            combined = combined.union(polygons[i])

        # if the geometry is still a polygon convert to MultiPolygon and return
        if isinstance(combined, Polygon):
            return Shape(geometry=MultiPolygon([combined]))

        #otherwise just return the polygon
        return Shape(geometry=combined)