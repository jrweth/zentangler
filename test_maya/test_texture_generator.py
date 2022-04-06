import sys
import pymel.core as pm

# this is just temporary until files get moved into python script folder
sys.path.append('/Users/wetherbe-admin/personal/projects/zentangler')
sys.path.append('/Users/wetherbe-admin/personal/projects/zentangler/zentangler')

from zentangler_maya.uv_shape_generator import UVShapeGenerator
from zentangler_maya.texture_generator import TextureGenerator
from zentangler.operators.split_operator import SplitOperator
from zentangler.operators.operator_parameter import OperatorParameterValue as OPV
from zentangler.shape import Shape
from shapely.geometry import Polygon, MultiPolygon

#create a pol torus
# pm.polyTorus()
# pm.select("pCube1")
obj =pm.ls(selection=True)[0]

# get the shape from the uvs
generator = UVShapeGenerator(obj)
shape = generator.get_silhouette_poly()

print ("got combined")

# run the split operator on the shape
split = SplitOperator([
    OPV(name="cross_split", value=True),
    OPV(name="angle", value=34)
])
shapes = split.execute([shape], ["splits"])

# generate and assign the texture
tg = TextureGenerator(obj, shapes)
tg.assign_texture()

pm.select(obj.name())