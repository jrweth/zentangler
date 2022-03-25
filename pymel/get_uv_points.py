import pymel.core as pm
from pymel.all import mel
import pymel.core

pm.select("pCube1")
cube = pm.ls(selection=True)[0]
#returns the num of verts in each face and corresponding uv index
#print(repr(cube.getAssignedUVs()))
#gets the uv coordinates x vals and y vals
#print(repr(cube.getUVs()))
#gets the shell to which each uv belongs
#print(repr(cube.getUvShellsIds()))


def getUvVertexId(obj, uvId):
    """
    get the vertexId associated with a uvId
    """
    uv = obj.getUV(uvId)
    for vert in obj.vtx:
        uvIds = vert.getUVIndices()
        for i in uvIds:
            if i == uvId:
                return vert.index()

def getUvIndexInUvShellBorder(objectName, shellIndex):
    #select the object
    pm.select(objectName)
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
    #get the shellId to which each UV belongs
    uvIdToShell = obj.getUvShellsIds()[0]
    
    shellBorderUvIds = getUvIndexInUvShellBorder("pCube1", shellIndex)
    
    #loop through vertices to see if which map to a uv in our shell
    vertIds = set()
    for v in obj.vtx:
        for uvId in v.getUVIndices():
            if uvId in shellBorderUvIds:
                vertIds.add(v.index())        
    return vertIds
    


def getEdgeIndexInUvShellBorder(objectName, shellIndex):
    #select the object
    pm.select(objectName)
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
    return {
        obj.e[edgeId].connectedVertices()[0].index(),
        obj.e[edgeId].connectedVertices()[1].index()
    }
    
def uvsShareBorderEdge(obj, uvId1, uvId2, borderEdgeIds):
    """
    Check if two UVs are connected via a shell border edges
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
   
    # order the shell UVs into separate ordered polygons pt orders
   
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




pm.select("pCube1")
cube = pm.ls(selection=True)[0]
shellIndex = 0
#vertIds = getVertIndexInUvShellBorder(cube, shellIndex)
uvIds = getUvIndexInUvShellBorder(cube, shellIndex)
edgeIds = getEdgeIndexInUvShellBorder("pCube1", shellIndex)
polygons = getBorderShellPolygons(cube, uvIds, edgeIds)
print(polygons)

