from zentangler.tangle import Tangle
from zentangler.grammar_manager import GrammarManager
from zentangler_maya.texture_generator import TextureGenerator
from zentangler_maya.uv_shape_generator import UVShapeGenerator
from zentangler.multi_tangle import MultiTangle
from zentangler_maya.tangle_editor import TangleEditor
from datetime import datetime

def create_tangle(obj, initial_shapes, grammar_filename,
                  override_png_filename=None,
                  assign_texture=False,
                  tangle_name="zentangle"
                  ):
    """
    Create a tangle associated with a given object
    Parameters:
        obj: pymel.core.general.PyNode
            object to associate the tangle with and assign texture to
        initial_shapes: list[zentangler.Shape]
            list of initial shapes to use for tangle creation
        grammar_filename: string
            the filename of the grammar file
        override_png_filename: str
            the name (with path) of the png file to output the texture to
        assign_texture: bool
            flag indicating if the texture should be assigned to the object once created
  
    """

    # parse grammar & rules
    grammar_manager = GrammarManager()
    if grammar_filename is None:
        grammar = grammar_manager.get_random_base_grammar(datetime.now().timestamp())
    else:
        grammar = grammar_manager.get_grammar(grammar_filename)
    
    # create tangle
    tangle = Tangle(initial_shapes, grammar, tangle_name)
    tangle.create()
    
    # create texture
    texture_gen = TextureGenerator(obj, tangle.history[-1].getShapesForNewExpansion(), override_png_filename)
    texture_gen.create_texture_file()

    #create the thumbnail
    filename = texture_gen.get_texture_file_name("png")
    thumbnail_filename = filename.replace(".png", "_thumbnail.png")
    texture_gen.override_png_filename = thumbnail_filename
    texture_gen.create_texture_file(256)
    texture_gen.override_png_filename = override_png_filename

    # assign texture if required
    if assign_texture:
        texture_gen.assign_texture()
    return {"tangle": tangle, "png_filename": texture_gen.get_texture_file_name("png")}


def create_silhouette_tangle(obj, grammar_filename, override_png_filename=None, tangle_name="zentangle", multi_uv_shells=False):
    """
    Create a tangle based upon the current silhouette of the object in the viewport
    Parameters:
        obj: pymel.core.general.PyNode
            object to associate the tangle with and assign texture to
        grammar_filename: string
            the filename of the grammar file
        override_png_filename: str
            the name (with path) of the png file to output the texture to
    """
    shape_gen = UVShapeGenerator(obj)
    if not multi_uv_shells:
        initial_shapes = [shape_gen.get_silhouette_shape()]
        if initial_shapes is not None:
            return create_tangle(obj, initial_shapes, grammar_filename, override_png_filename, assign_texture=True, tangle_name=tangle_name)
    else:
        initial_shapes_list = shape_gen.get_silhouette_uv_shell_shapes()
        if initial_shapes_list is not None:
            multi_tangle = MultiTangle([], tangle_name)
            multi_tangle.init_from_shape_lists_cycle_grammars(initial_shapes_list)
            multi_tangle.create_all()
            texture_gen = TextureGenerator(obj,
                                           multi_tangle.get_last_expansion_shapes(),
                                           TangleEditor.get_img_folder_from_name(tangle_name) + "/tangle.png")
            texture_gen.assign_texture()
            return {"tangle": multi_tangle}



def create_uv_map_tangle(obj, grammar_filename, override_png_filename=None, tangle_name="zentangle", multi_uv_shells=False):
    """
    Create a tangle based upon the current uv map set selected and assign the generated texture
    Parameters:
        obj: pymel.core.general.PyNode
            object to associate the tangle with and assign texture to
        grammar_filename: string
            the filename of the grammar file
        override_png_filename: str
            the name (with path) of the png file to output the texture to
    """
    shape_gen = UVShapeGenerator(obj)
    if not multi_uv_shells:
        initial_shapes = [shape_gen.get_current_uv_shape()]
        if initial_shapes is not None:
            return create_tangle(obj, initial_shapes, grammar_filename, override_png_filename, assign_texture=True, tangle_name=tangle_name)
    else:
        initial_shapes_list = shape_gen.get_current_uv_shell_shapes()
        if initial_shapes_list is not None:
            multi_tangle = MultiTangle([], tangle_name)
            multi_tangle.init_from_shape_lists_cycle_grammars(initial_shapes_list)
            multi_tangle.create_all()
            texture_gen = TextureGenerator(obj, multi_tangle.get_last_expansion_shapes(), override_png_filename)
            texture_gen.assign_texture()
            return {"tangle": multi_tangle}

