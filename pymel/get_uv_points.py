import pymel.core as pm
from pymel.all import mel

pm.select("pCube1")
cube = pm.ls(selection=True)[0]
#returns the num of verts in each face and corresponding uv index
print(repr(cube.getAssignedUVs()))
#gets the uv coordinates x vals and y vals
print(repr(cube.getUVs()))
#gets the shell to which each uv belongs
print(repr(cube.getUvShellsIds()))

#get the indexes of the verticies in the shell border
def getVertIndexInUvShellBorder(object, shellIndex):
    return []
    
def getUvIndexInUvShellBorder(object, shellIndex):
    return []
    
def getEdgeIndexInUvShellBorder(object, shellIndex):
    return[]

mel.eval("changeSelectMode -component; selectType -ocm -alc false; selectType -alc false; selectType -puv true; SelectUVBorderComponents;")
uvs = pm.ls(selection=True, flatten=True)
uvIndexes = []
for uv in uvs:
    uvIndexes.append(uv.index())
    print(repr(cube.getUV(uv.index())))
print (uvIndexes)

mel.eval("changeSelectMode -component; selectType -ocm -alc false; selectType -alc false; selectType -vertex true; SelectUVBorderComponents;")
vrtxs = pm.ls(selection=True, flatten=True)
vrtxIndexes = []
for vrtx in vrtxs:
    vrtxIndexes.append(vrtx.index())
    print(repr(vrtx.connectedVertices()))
print (vrtxIndexes)