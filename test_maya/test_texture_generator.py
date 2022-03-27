import sys
import pymel.core as pm

# this is just temporary until files get moved into python script folder
sys.path.append('/Users/wetherbe-admin/personal/projects/zentangler')
sys.path.append('/Users/wetherbe-admin/personal/projects/zentangler/zentangler')

from zentangler_maya.uv_shape_generator import UVShapeGenerator
from zentangler_maya.texture_generator import TextureGenerator
from zentangler.operator.split_operator import SplitOperator
from zentangler.operator.operator_parameter import OperatorParameterValue as OPV

#create a poly torus
pm.polyTorus()
obj = pm.ls(selection=True)[0]

# get the shape from the uvs
generator = UVShapeGenerator(obj)
shape = generator.get_shape()

# run the split operator on the shape
split = SplitOperator([
    OPV(name="cross_split", value="true"),
    OPV(name="angle", value=85)
])
shapes = split.execute([shape], ["splits"])

# generate and assign the texture
tg = TextureGenerator(obj, shapes)
tg.assign_texture()

pm.select(obj.name())