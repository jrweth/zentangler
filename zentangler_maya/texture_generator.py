from zentangler.svg import SVG
from zentangler.shape import Shape
import pymel.core as pm
import os

class TextureGenerator():
    """
    Class which takes a test_maya node object and a list of generated zentangle shapes and
    creates a texture image and creates a material and shader to shade that image
    """

    def __init__(self, obj, generated_shapes):
        """
        initialize the texture generator with the object and generated shapes
        Parameters:
            obj: test_maya.core.general.PyNode
                the object for which the texture is being generated
            generated_shapes:
                the list of zentangler Shapes to add to the texture
        """
        self.obj: pm.general.PyNode = obj
        self.generated_shapes: list[Shape] = generated_shapes

    def get_texture_file_name(self, type="png"):
        """
        get the name of the texture files (png or svg) will create a folder in the current
        maya project to hold the images

        Parameters:
            type: string
                the file type (svg, png) of the texture file
        """
        folderPath = pm.workspace.getPath() + "/zentangler"
        # if no zentangler folder exists for this project then make one
        if not os.path.isdir(folderPath):
            os.mkdir(folderPath)
        return folderPath + "/zentangler_" + self.obj.name() + "." + type


    def create_texture_file(self):
        """
        create the svg and png textures files for the object and generated shapes
        """
        file_path_svg = self.get_texture_file_name("svg")
        file_path_png = self.get_texture_file_name("png")
        svg = SVG(file_path_svg)
        for shape in self.generated_shapes:
            svg.add_shape(shape)
        svg.save_png(file_path_png)

    def assign_texture(self):
        """
        generate texture and create shader/material/texture file nodes to shade the object
        """
        self.create_texture_file()
        prefix = "zenTangler_" + self.obj.name() + "_gen"

        # Deleting existing shader/material nodes
        existing_textures = pm.ls(prefix + "*")
        if len(existing_textures) > 0:
            pm.delete(existing_textures)

        # create a new material node
        mat_name = prefix + "_Mat"
        mat = pm.shadingNode('standardSurface', asShader=1, name=mat_name)

        # create the shader node and hook up the material
        shader_name = prefix + "_Shader"
        shader = pm.sets(renderable=1, noSurfaceShader=1, empty=1, name=shader_name)
        mat.outColor >> shader.surfaceShader
        shape = self.obj.getShape()
        pm.sets(shader, edit=True, forceElement=shape)

        # create the texture file node and set it to the material base color
        texture_file_name = prefix + "_TextureFile"
        texture_file = pm.shadingNode('file', name=texture_file_name, asTexture=True, isColorManaged=True)
        pm.connectAttr(texture_file + ".outColor", mat + ".baseColor")

        # set the generated png file as the image path
        png_name = self.get_texture_file_name("png")
        texture_file.setAttr("fileTextureName", png_name)
