import pymel.core as pm
from pymel.all import mel
import pymel.core



def getUvVertexId(obj, uvId):
    """
    get the vertexId associated with a uvId
    
    return: int
        the MeshVertex index associated with the uv
      
    Paramters:
        obj: pymel.core.Node
           python node object representing the 3D shape
        uvId:
            the MeshUV index
    """
    uv = obj.getUV(uvId)
    for vert in obj.vtx:
        uvIds = vert.getUVIndices()
        for i in uvIds:
            if i == uvId:
                return vert.index()

def getUvIndexInUvShellBorder(obj, shellIndex):
    """
    Get the UV indices that are in the UV Shell border
        
    return:
        set of UV indices that make up the shell border edge
    
    Parameters:
        obj: pymel.core.Node
           python node object representing the 3D shape
        shellIndex:
            the uv shell index
    """
    
    #select the object
    pm.select(obj.name())
    obj = pm.ls(selection=True)[0]
    
    mel.eval("changeSelectMode -component; selectType -ocm -alc false; selectType -alc false; selectType -puv true; selectType -suv true; SelectUVBorderComponents;")
    uvs = pm.ls(selection=True, flatten=True)
 
    uvIdToShell = obj.getUvShellsIds()[0]
 
    ids = set()
    for uv in uvs:
        if uvIdToShell[uv.index()] == shellIndex:   
            ids.add(uv.index())
        
    return ids

def getVertIndexInUvShellBorder(obj, shellIndex):
    """
    Get the vertices that in in the UV Shell border
        
    return:
        set of MeshEdge indices that make up the shell border edge
    
    Parameters:
        obj: pymel.core.Node
           python node object representing the 3D shape
        shellIndex:
            the uv shell index
    """
    #get the shellId to which each UV belongs
    uvIdToShell = obj.getUvShellsIds()[0]
    
    shellBorderUvIds = getUvIndexInUvShellBorder(obj, shellIndex)
    
    #loop through vertices to see if which map to a uv in our shell
    vertIds = set()
    for v in obj.vtx:
        for uvId in v.getUVIndices():
            if uvId in shellBorderUvIds:
                vertIds.add(v.index())        
    return vertIds
    


def getEdgeIndexInUvShellBorder(obj, shellIndex):
    """
    Get all the edge indices in a UV shell border
    
    return:
        set of MeshEdge indices that make up the shell border edge
        
    Parameters:
        obj: pymel.core.Node
           python node object representing the 3D shape
        shellIndex:
            the uv shell index
        
    """
    #select the object
    pm.select(obj.name())
    obj = pm.ls(selection=True)[0]
    
    #select all the vertex in uv borders
    mel.eval("changeSelectMode -component; selectType -ocm -alc false; selectType -alc false; selectType -edge true; SelectUVBorderComponents;")
    borderEdges = pm.ls(selection=True, flatten=True)
    #get the verts in our shell
    shellVerts = getVertIndexInUvShellBorder(obj, shellIndex)
    
    #loop through the border edges and return the ones for which both verts are in the shell
    edgeIds = set()
    for edge in borderEdges:
        verts = edge.connectedVertices()
        if verts[0].index() in shellVerts and verts[1].index() in shellVerts:
            edgeIds.add(edge.index())
 
    return edgeIds
    
    


def getEdgeVertexIds(obj, edgeId):
    """
    Get the tuple of vertex indices defining a MeshEdge in the object
    
    return:
        tuple containing the two points defining the line
        
    Parameters:
       obj: pymel.core.Node
           python node object representing the 3D shape
       edgeId: int
           index of the MeshEdge in the object
    """
    return {
        obj.e[edgeId].connectedVertices()[0].index(),
        obj.e[edgeId].connectedVertices()[1].index()
    }
    
def uvsShareBorderEdge(obj, uvId1, uvId2, borderEdgeIds):
    """
    Check if two UVs are connected via a shell border edge
    
    Parameters:
        obj: Node
            the Node object containing the geometry
        uvId1: int
            the index of the uv to check
        uvId2: int
            the index of the second uv to check
        borderEdgeIds: int[]
            ids of the MeshEdge which are in the uv shell border
        
    """
    vtxId1 = getUvVertexId(obj, uvId1)
    vtxId2 = getUvVertexId(obj, uvId2)
    
    uvVertices = {vtxId1, vtxId2}
    
    # loop through border edges and make sure there is a border edge that contains both vertices
    for edgeId in borderEdgeIds:
        edgeVertices = getEdgeVertexIds(obj, edgeId)
        if len(uvVertices.difference(edgeVertices)) == 0: 
            return True
    return False

      
def getBorderShellPolygons(obj, shellUvIds, borderEdgeIds):
   """
   take all the uvs in a shell border and order them so that that trace the outline of the polygons (both outer and inner "hole" polygons)
   
   return: list[list[int]]
       list of polygons and their ordererd uv_ids (e.g. [ [0,1,3,2], [4,5,7,6] ] ) 
   
   Parameters:
       obj: pymell.cored.node
           python node object representing the 3D shape
       shellUvIds: int[]
           list of UV indices in the uv shell border polygon
       borderEdgeIds: int[]
           list of MeshEdge indices that define the border of the UV shell
   """

   
    remaining = shellUvIds.copy()
    currUvId = remaining.pop()
    currPolygonId = 0
    polygons = [[currUvId]]

    while len(remaining) > 0:
        # loop through the uvIds and find connecting ones
        uvIdsConnected = set()
        for uvId in remaining:
            if uvsShareBorderEdge(obj, currUvId, uvId, borderEdgeIds):
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
            minDist = 100
            minId = -1
            currUv = obj.getUV(currUvId)
            # todo: this is a bit suspect as the nearets UV might not always be the connected one
            for uvId in uvIdsConnected:
                uv = obj.getUV(uvId)
                dist = pow(currUv[0] - uv[0], 2) + pow(currUv[1] - uv[1], 2)
                #print ("dist", currUvId, uvId, dist, currUv, uv)
                if dist < minDist:
                    minId = uvId
                    minDist = dist
            currUvId = minId
            polygons[currPolygonId].append(minId)
            remaining.difference_update({minId})
 
    return polygons



#test for running on a stock cylinder
pm.select("pCylinder1")
obj = pm.ls(selection=True)[0]

for shellIndex in range(obj.getUvShellsIds()[1]):
    uvIds = getUvIndexInUvShellBorder(obj, shellIndex)
    edgeIds = getEdgeIndexInUvShellBorder(obj, shellIndex)
    polygons = getBorderShellPolygons(obj, uvIds, edgeIds)
    for p in polygons:
        print ("poly", p)
        for uvId in p:
            print (obj.getUV(uvId))
