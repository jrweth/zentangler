import pymel.core as pm
from pymel.all import mel
from zentangler.shape import Shape
from shapely.geometry import MultiPolygon, Polygon


class UVShapeGeneratorOrig:
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
        self.uv_adjacent_map = {}

    def get_uv_vertex_id(self, uvId):
        """
        get the vertexId associated with a uvId

        return: int
            the MeshVertex index associated with the uv

        Paramters:
            obj: test_maya.core.general.PyNode
               python node object repesenting the 3D shape
            uvId:
                the MeshUV index
        """
        uv = self.obj.getUV(uvId)
        for vert in self.obj.vtx:
            uvIds = vert.getUVIndices()
            for i in uvIds:
                if i == uvId:
                    return vert.index()

    def get_uv_vertex_map(self):
        """
        get a UV to Vertex Map for an object

        Parameters:
            obj: test_maya.core.general.PyNode
                the maya object holding the geometry

        return:  dict[uvId] => vertexId
        """
        vtxMap = {}
        for vId in range(len(self.obj.vtx)):
            for uvId in self.obj.vtx[vId].getUVIndices():
                vtxMap[uvId] = vId
        return vtxMap

    def get_uv_adjacent_map(self):

        # if we've already done the map don't do it again
        if len(self.uv_adjacent_map) > 0:
            return self.uv_adjacent_map

        self.uv_adjacent_map = {}
        self.uv_face_map = {}
        for f in self.obj.f:
            for v_index in range(f.numVertices()):
                uv_id_1 = f.getUVIndex(v_index)

                # if we are at the last vertex connect it back to the first
                if v_index == f.numVertices() - 1:
                    uv_id_2 = f.getUVIndex(0)
                else:
                    uv_id_2 = f.getUVIndex(v_index + 1)

                # add uvid2 to uvid1s adjacent list
                if not uv_id_1 in self.uv_adjacent_map:
                    self.uv_adjacent_map[uv_id_1] = {uv_id_2}
                else:
                    self.uv_adjacent_map[uv_id_1].add(uv_id_2)

                # add uvid1 to uvid2 adjacent list
                if not uv_id_2 in self.uv_adjacent_map:
                    self.uv_adjacent_map[uv_id_2] = {uv_id_1}
                else:
                    self.uv_adjacent_map[uv_id_2].add(uv_id_1)
        return self.uv_adjacent_map

    def get_uv_indices_in_uv_shell_border(self, shellIndex):
        """
        Get the UV indices that are in the UV Shell border

        return:
            set of UV indices that make up the shell border edge

        Parameters:
            obj: test_maya.core.general.PyNode
               python node object representing the 3D shape
            shellIndex:
                the uv shell index
        """

        # select the object
        pm.select(self.obj.name())
        obj = pm.ls(selection=True)[0]

        mel.eval(
            "changeSelectMode -component; selectType -ocm -alc false; selectType -alc false; selectType -puv true; selectType -suv true; SelectUVBorderComponents;")
        uvs = pm.ls(selection=True, flatten=True)

        uvIdToShell = self.obj.getUvShellsIds()[0]

        ids = set()
        for uv in uvs:
            if uvIdToShell[uv.index()] == shellIndex:
                ids.add(uv.index())

        return ids

    def get_vertex_indices_in_uv_shell_border(self, shellIndex):
        """
        Get the vertices that in in the UV Shell border

        return:
            set of MeshEdge indices that make up the shell border edge

        Parameters:
            obj: test_maya.core.general.PyNode
               python node object representing the 3D shape
            shellIndex:
                the uv shell index
        """
        # get the shellId to which each UV belongs
        uvIdToShell = self.obj.getUvShellsIds()[0]

        shellBorderUvIds = self.get_uv_indices_in_uv_shell_border(shellIndex)

        # loop through vertices to see if which map to a uv in our shell
        vertIds = set()
        for v in self.obj.vtx:
            for uvId in v.getUVIndices():
                if uvId in shellBorderUvIds:
                    vertIds.add(v.index())
        return vertIds

    def get_edge_indices_in_uv_shell_border(self, shellIndex):
        """
        Get all the edge indices in a UV shell border

        return:
            set of MeshEdge indices that make up the shell border edge

        Parameters:
            obj: test_maya.core.general.PyNode
               python node object representing the 3D shape
            shellIndex:
                the uv shell index

        """
        # select the object
        pm.select(self.obj.name())
        obj = pm.ls(selection=True)[0]

        # select all the vertex in uv borders
        mel.eval(
            "changeSelectMode -component; selectType -ocm -alc false; selectType -alc false; selectType -edge true; SelectUVBorderComponents;")
        borderEdges = pm.ls(selection=True, flatten=True)
        # get the verts in our shell
        shellVerts = self.get_vertex_indices_in_uv_shell_border(shellIndex)

        # loop through the border edges and return the ones for which both verts are in the shell
        edgeIds = set()
        for edge in borderEdges:
            verts = edge.connectedVertices()
            if verts[0].index() in shellVerts and verts[1].index() in shellVerts:
                edgeIds.add(edge.index())

        return edgeIds

    def get_edge_vertex_ids(self, edgeId):
        """
        Get the tuple of vertex indices defining a MeshEdge in the object

        return:
            tuple containing the two points defining the line

        Parameters:
           obj: test_maya.core.general.PyNode
               python node object representing the 3D shape
           edgeId: int
               index of the MeshEdge in the object
        """
        return {
            self.obj.e[edgeId].connectedVertices()[0].index(),
            self.obj.e[edgeId].connectedVertices()[1].index()
        }

    def get_edge_vertex_map(self, edgeIds):
        """
        create a map for looking up the vertices for the set of edges

        return: map[edgeId] -> set(edgeVerticies)

        Paramteters:
            obj: test_maya.core.general.PyNode
                python node object representing the 3D shape
            edgeIds:
                indexes for the edges to perform the map for
        """
        vtxMap = {}
        for edgeId in edgeIds:
            vtxMap[edgeId] = self.get_edge_vertex_ids(edgeId)

        return vtxMap

    def uvs_share_border_edge(self, uvId1, uvId2, borderEdgeIds, uvVertexMap, edgeVertexMap):
        """
        Check if two UVs are connected via a shell border edge

        Parameters:
            obj: test_maya.core.general.PyNode
                the Node object containing the geometry
            uvId1: int
                the index of the uv to check
            uvId2: int
                the index of the second uv to check
            borderEdgeIds: int[]
                ids of the MeshEdge which are in the uv shell border

        """
        vtxId1 = uvVertexMap[uvId1]
        vtxId2 = uvVertexMap[uvId2]

        #if it is the same vertex than the don't actually share an edge
        if vtxId1 == vtxId2:
            return False

        uvVertices = {vtxId1, vtxId2}

        # loop through border edges and make sure there is a border edge that contains both vertices
        for edgeId in borderEdgeIds:
            edgeVertices = edgeVertexMap[edgeId]
            if len(uvVertices.difference(edgeVertices)) == 0:
                return True
        return False

    def get_border_shell_polygons(self, shellUvIds, borderEdgeIds):
        """
        take all the uvs in a shell border and order them so that that trace the outline of the polygons (both outer and inner "hole" polygons)

        return: list[list[int]]
            list of polygons and their ordererd uv_ids (e.g. [ [0,1,3,2], [4,5,7,6] ] )

        Parameters:
            obj: test_maya.core.general.PyNode
                python node object representing the 3D shape
            shellUvIds: int[]
                list of UV indices in the uv shell border polygon
            borderEdgeIds: int[]
                list of MeshEdge indices that define the border of the UV shell
        """

        uvVertexMap = self.get_uv_vertex_map()
        uv_adjacent_map = self.get_uv_adjacent_map()
        edgeVertexMap = self.get_edge_vertex_map(borderEdgeIds)
        remaining = shellUvIds.copy()
        currUvId = remaining.pop()
        currPolygonId = 0
        polygons = [[currUvId]]

        while len(remaining) > 0:
            # loop through the uvIds and find connecting ones
            uvIdsConnected = set()
            for uvId in uv_adjacent_map[currUvId]:
                if uvId in remaining:
                    if self.uvs_share_border_edge(currUvId, uvId, borderEdgeIds, uvVertexMap, edgeVertexMap) and  1 == 1:
                        uvIdsConnected.add(uvId)
            # if no uvs added start another polygon
            if len(uvIdsConnected) == 0:
                currUvId = remaining.pop()
                polygons.append([currUvId])
                currPolygonId = len(polygons) - 1
            # only one connection found - must be the one
            elif len(uvIdsConnected) == 1:
                currUvId = uvIdsConnected.pop()
                polygons[currPolygonId].append(currUvId)
                remaining.difference_update({currUvId})
            # more than one connection found - get the closest one
            else:
                print ("more than one")
                minDist = 100
                minId = -1
                currUv = self.obj.getUV(currUvId)
                # todo: this is a bit suspect as the nearets UV might not always be the connected one
                for uvId in uvIdsConnected:
                    uv = self.obj.getUV(uvId)
                    dist = pow(currUv[0] - uv[0], 2) + pow(currUv[1] - uv[1], 2)
                    # print ("dist", currUvId, uvId, dist, currUv, uv)
                    if dist < minDist:
                        minId = uvId
                        minDist = dist
                currUvId = minId
                polygons[currPolygonId].append(minId)
                remaining.difference_update({minId})

        good_polygons = []
        for p in polygons:
            if (len(p) > 2):
                good_polygons.append(p)
            else:
                pr
        return good_polygons

    def get_outer_polygon_index(self, obj, polygons):
        """
        given an array of polygon shells uv points - get the index of the outermost
        """
        # From a list of polygons find the one that contains all the rest

        index = -1
        minX = 100
        minY = 100
        maxX = -100
        maxY = -100

        for i in range(len(polygons)):
            for uvId in polygons[i]:
                pt = obj.getUV(uvId)
                if pt[0] < minX:
                    minX = pt[0]
                    index = i

                if pt[0] > maxX:
                    maxX = pt[0]
                    index = i

                if pt[1] < minY:
                    minY = pt[1]
                    index = i

                if pt[1] > maxY:
                    maxY = pt[1]
                    index = i
        return index

    def uvs_to_points(self, uvIds):
        """
        Take a list of object UV ids and convert them to point tuples

        Parameters:
            uvIds: int[]
                list of uvIds to convert to points
        """
        points = []
        for uvId in uvIds:
            points.append(self.obj.getUV(uvId))
        return points

    def border_shell_polygons_to_shapely_polygon(self, borderShellPolygons):
        """
        take the list of uv shell border polygons (representing boundaries and holes)
        and return a shapely polygon

        Parameters:
            borderShellPolygons: polygons[float[]]
        """
        outerPolygonIndex = self.get_outer_polygon_index(self.obj, borderShellPolygons)
        outerShell = self.uvs_to_points(borderShellPolygons[outerPolygonIndex])
        holes = []

        # loop through the "hole" polygons and add them to our secondary polygon array
        for i in range(len(borderShellPolygons)):
            if not i == outerPolygonIndex:
                holes.append(self.uvs_to_points(borderShellPolygons[i]))

        return Polygon(outerShell, holes)
    def get_shape(self):
        """
        get the shapely shape representing all the separate polygon shells found in the UV mapping
        """
        polygons = []
        for shellIndex in range(self.obj.getUvShellsIds()[1]):
            # get the uvIDs in the shell border and shell hole borders
            uvIds = self.get_uv_indices_in_uv_shell_border(shellIndex)
            # get the edge ids in the shell border and shell hold borders
            edgeIds = self.get_edge_indices_in_uv_shell_border(shellIndex)
            # get the polygons representing the shell border and holes
            borderShellPolygons = self.get_border_shell_polygons(uvIds, edgeIds)
            polygons.append(self.border_shell_polygons_to_shapely_polygon(borderShellPolygons))

        # return the combined shape of all the polygons shells found
        return Shape(geometry=MultiPolygon(polygons))
