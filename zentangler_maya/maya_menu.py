import pymel.core as pm
from pymel.core.windows import image
import os
import sys

from zentangler.tangle import Tangle
from zentangler_maya.tangle_creation import create_uv_map_tangle, create_silhouette_tangle
from zentangler.svg import SVG
import zentangler_maya.rule_editor as rule_editor
from zentangler.grammar import BASE_GRAMMARS

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


def add_rules_to_ui(tangle):
    i = 0
    rules = tangle.grammar.rules
    global rules_scroll
    rules_scroll = pm.scrollLayout()

    with rules_scroll:
        with pm.columnLayout(adjustableColumn=True, height=2000):
            pm.text("Tangle Grammar Editor")

            for rule in rules:
                rule_editor.add_grammar_rule_widget(0, i, rule, tangle)     # todo: uv_shell_index
                i += 1

    pm.setParent(window)
    pm.showWindow(window)


def add_tangle_to_ui(main_layout):
    global tangle_image
    global refresh_button

    image_path = tangle_info.get("png_filename")
    thumbnail_path = image_path.replace(".png", "_thumbnail.png")

    with main_layout:
        with pm.columnLayout(adjustableColumn=False, rowSpacing=10):
            tangle_image = pm.image("tangle_image", image=thumbnail_path, backgroundColor=[0.5, 0.5, 0.5], width=256)
            refresh_button = pm.button("Refresh Tangle", command=pm.Callback(refresh_tangle, tangle_info, selectedObj))

    pm.setParent(window)
    pm.showWindow(window)

    add_rules_to_ui(tangle)


def refresh_tangle(tangle_info, selectedObj):
    tangle_info['tangle'].create()
    png_path = tangle_info['png_filename']
    svg_path = png_path.replace(".png", ".svg")
    thumbnail_path = png_path.replace(".png", "_thumbnail.png")
    svg = SVG(svg_path)
    for shape in tangle.history[-1].getShapesForNewExpansion():
        svg.add_shape(shape)
    svg.save_png(png_path, 1024)
    svg.save_png(thumbnail_path, 256)
    tangle_image.setImage(thumbnail_path)
    pm.select(selectedObj)


def create_tangles_from_selected(base_grammar, uv_type_radios, main_layout, grammar_picker):
    global tangle_info
    global selectedObj
    global tangle
    global grammar_options
    global tangle_image
    global tangle_already_created

    if tangle_already_created:
        pm.deleteUI(tangle_image, refresh_button, rules_scroll)

    if grammar_picker.getValue() == "random grammar":
        grammar_filename = None
    else:
        for grammar_def in BASE_GRAMMARS:
            if grammar_def["name"] == grammar_picker.getValue():
                grammar_filename = grammar_def["path"]

    # make sure we have some objects selected
    selectedObj = pm.ls(sl=True)[0]

    if uv_type_radios.getSelect() == 1:
        tangle_info = create_uv_map_tangle(selectedObj, grammar_filename=grammar_filename)
    elif uv_type_radios.getSelect() == 2:
        tangle_info = create_silhouette_tangle(selectedObj, grammar_filename=grammar_filename)

    tangle = tangle_info.get("tangle")

    add_tangle_to_ui(main_layout)

    if not tangle_already_created:
        tangle_already_created = True;

    pm.select(selectedObj)

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

        pm.button("Create", command=pm.Callback(create_tangles_from_selected, grammar, uv_type, main_layout, grammar_picker))

        if tangle_already_created:
            add_tangle_to_ui(main_layout)

    pm.setParent('..')
    pm.showWindow(window)


def add_zentangler_menu():
    if pm.menu('ZenTanglerMenu', exists=True): pm.deleteUI('ZenTanglerMenu')

    g_main_window = pm.melGlobals['gMainWindow']

    menu = pm.menu('ZenTanglerMenu',
                   label="ZenTangler",
                   parent=g_main_window,
                   tearOff=True,
                   allowOptionBoxes=True
                   )

    pm.menuItem(l='Create', p=menu, c=pm.Callback(create_tangle_window))

    global tangle_already_created
    tangle_already_created = False

add_zentangler_menu()