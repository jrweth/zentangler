import pymel.core as pm
from pymel.core.windows import image
import re
from zentangler_maya.config_editor import ConfigEditor

from zentangler.tangle import Tangle
from zentangler_maya.tangle_creation import create_uv_map_tangle, create_silhouette_tangle
from zentangler_maya.tangle_editor import TangleEditor
from zentangler.grammar import BASE_GRAMMARS
from zentangler.multi_tangle import MultiTangle
from zentangler_maya.multi_tangle_editor import MultiTangleEditor

window: None
selectedObj: None
tangle_info: dict
tangle: Tangle
tangle_image: image
refresh_button: None
rules_scroll: None
tangle_already_created: None

'''Paste in Maya Script Editor
import importlib
from zentangler_maya import rule_editor
from zentangler_maya import maya_menu
importlib.reload(maya_menu)
importlib.reload(rule_editor)
'''


# def add_rules_to_ui(tangle):
#     i = 0
#     rules = tangle.grammar.rules
#     global rules_scroll
#     rules_scroll = pm.scrollLayout()
#
#     with rules_scroll:
#         with pm.columnLayout(adjustableColumn=True, height=2000):
#             pm.text("Tangle Grammar Editor")
#
#             for rule in rules:
#                 rule_editor.add_grammar_rule_widget(0, i, rule, tangle)     # todo: uv_shell_index
#                 i += 1
#
#     pm.setParent(window)
#     pm.showWindow(window)


def add_tangle_to_ui(tangle_layout):
    global tangle_image
    global refresh_button

    for child in tangle_layout.children():
        pm.deleteUI(child)

    if isinstance(tangle, Tangle):
        TangleEditor(tangle_layout, tangle)
    elif isinstance(tangle, MultiTangle):
        MultiTangleEditor(tangle_layout, tangle)


# def refresh_tangle(tangle_info, selectedObj):
#     tangle_info['tangle'].create()
#     png_path = tangle_info['png_filename']
#     svg_path = png_path.replace(".png", ".svg")
#     thumbnail_path = png_path.replace(".png", "_thumbnail.png")
#     svg = SVG(svg_path)
#     for shape in tangle.history[-1].getShapesForNewExpansion():
#         svg.add_shape(shape)
#     svg.save_png(png_path, 1024)
#     svg.save_png(thumbnail_path, 256)
#     tangle_image.setImage(thumbnail_path)
#     pm.select(selectedObj)


def create_tangles_from_selected(base_grammar, uv_type_radios, tangle_layout, grammar_picker, uv_shells):
    global tangle_info
    global selectedObj
    selected_objs = []
    global tangle
    global grammar_options
    global tangle_image
    global tangle_already_created

    # clear out previous tangle editors if they exist
    for child in tangle_layout.children():
        pm.deleteUI(child)


    if grammar_picker.getValue() == "random grammar":
        grammar_filename = None
    else:
        for grammar_def in BASE_GRAMMARS:
            if grammar_def["name"] == grammar_picker.getValue():
                grammar_filename = grammar_def["path"]

    # make sure we have some objects selected
    # selectedObj = pm.ls(sl=True)[0]
    selected_objs = pm.ls(sl=True)
    if len(selected_objs) > 0:
        selectedObj = selected_objs[0]
    else:
        # pm.promptDialog(
        #     title='Warning',
        #     message='No object selected! Please select an object before trying to create a tangle.',
        #     button=['OK'],
        #     defaultButton='OK')
        pm.confirmDialog(title='No object selected!', message='Please select an object before trying to create a tangle.', button=['OK'], defaultButton='OK')

        return

    multi_uv_shells = pm.checkBox(uv_shells, query=True, value=True)

    # create tangle name from object name but remove non-letters and numbers
    tangle_name = re.sub(r'[^a-zA-Z0-9]', '_', selectedObj.name())
    override_png_filename = TangleEditor.get_png_filename_from_name(tangle_name)

    if uv_type_radios.getSelect() == 1:
        tangle_info = create_uv_map_tangle(selectedObj,
                                           grammar_filename=grammar_filename,
                                           override_png_filename=override_png_filename,
                                           tangle_name=tangle_name,
                                           multi_uv_shells=multi_uv_shells
                                           )
    elif uv_type_radios.getSelect() == 2:

        tangle_info = create_silhouette_tangle(selectedObj,
                                           grammar_filename=grammar_filename,
                                           override_png_filename=override_png_filename,
                                           tangle_name=tangle_name,
                                           multi_uv_shells=multi_uv_shells
                                           )


    tangle = tangle_info.get("tangle")

    add_tangle_to_ui(tangle_layout)

    if not tangle_already_created:
        tangle_already_created = True

    pm.select(selectedObj)

    #tangle_info["tangle"].name = selectedObj.name()
    #tangle_editor = TangleEditor(main_layout, tangle_info["tangle"])



def update_selected_grammar(grammar_icon_ui, *args):
    """
    update the grammar icon whne a new grammar is selected
    """
    for grammar_def in BASE_GRAMMARS:
        if grammar_def["name"] == args[0]:
            grammar_icon_ui.setImage(grammar_def["icon_path"])


def create_tangle_window():
    '''Remote Debug Connection Code'''
    # # This should be the path your PyCharm installation
    # pydevd_egg = r"/Applications/PyCharm.app/Contents/debug-eggs/pycharm-debug.egg"
    # if not pydevd_egg in sys.path:
    #     sys.path.append(pydevd_egg)
    # import pydevd
    # # This clears out any previous connection in case you restarted the debugger from PyCharm
    # pydevd.stoptrace()
    # # 9001 matches the port number that I specified in my configuration
    # pydevd.settrace('localhost', port=9001, stdoutToServer=True, stderrToServer=True, suspend=False)

    # if the window already exists then delete it
    if pm.window('CreateZenTangleWindow', exists=True):
        pm.deleteUI("CreateZenTangleWindow")

    global window
    global tangle_already_created

    window = pm.window('CreateZenTangleWindow', title="Create ZenTangle", iconName='ZTangler', widthHeight=(400, 400))
    main_layout = pm.columnLayout(adjustableColumn=True, rowSpacing=10, columnWidth=250)
    with main_layout:
        pm.text("Select object(s) to create the tangle.")

        grammar_icon_ui = pm.image(image=BASE_GRAMMARS[0]["icon_path"], backgroundColor=[0.5, 0.5, 0.5], width=100, height=100)
        grammar_picker = pm.optionMenu(label='Select Grammar: ', changeCommand=pm.CallbackWithArgs(update_selected_grammar, grammar_icon_ui))
        for grammar in BASE_GRAMMARS:
            pm.menuItem(label=grammar["name"])
        pm.menuItem(label="random grammar")

        pm.text(label="Apply as: ", align="left")
        uv_type = pm.radioButtonGrp(
            labelArray2=["Current UV Map", "Scene Silhouette"],
            numberOfRadioButtons=2,
            select=1
        )
        uv_shells = pm.checkBox(label="tangle for each uv shell")

        create_button = pm.button("Create")
        tangle_layout = pm.columnLayout(adjustableColumn=False, rowSpacing=10)
        pm.button(create_button, edit=True,command=pm.Callback(create_tangles_from_selected, grammar, uv_type, tangle_layout, grammar_picker, uv_shells))


        if tangle_already_created:
            add_tangle_to_ui(tangle_layout)

    pm.setParent('..')
    pm.showWindow(window)

def create_config_window():
    print("creating config window")
    ConfigEditor()

def remove_zentangler_menu():
    if pm.menu('ZenTanglerMenu', exists=True):
        pm.deleteUI('ZenTanglerMenu')

def add_zentangler_menu():
    remove_zentangler_menu()

    g_main_window = pm.melGlobals['gMainWindow']

    menu = pm.menu('ZenTanglerMenu',
                   label="ZenTangler",
                   parent=g_main_window,
                   tearOff=True,
                   allowOptionBoxes=True
                   )

    pm.menuItem(l='Create', p=menu, c=pm.Callback(create_tangle_window))
    pm.menuItem(l='Set Configuration', p=menu, c=pm.Callback(create_config_window))

    global tangle_already_created
    tangle_already_created = False
