import pymel.core as pm
import os
import sys

from zentangler.tangle import Tangle
from zentangler_maya.tangle_creation import create_uv_map_tangle, create_silhouette_tangle
import zentangler_maya.rule_editor as rule_editor

window: None
selectedObj: None
tangle_info: dict
tangle: Tangle

'''Paste in Maya Script Editor
import importlib
from zentangler_maya import maya_menu
importlib.reload(maya_menu)
'''


def add_rules_to_ui():
    global tangle
    i = 0
    rules = tangle.grammar.rules

    with pm.columnLayout(adjustableColumn=True):
        pm.text("2")
    pm.setParent(window)
    pm.showWindow(window)

    with pm.columnLayout(adjustableColumn=True):
        pm.text("Tangle Grammar Editor")

        for rule in rules:
            rule_editor.add_grammar_rule_widget(0, i, rule)     # todo: uv_shell_index
            i += 1

    pm.setParent(window)
    pm.showWindow(window)


def create_tangles_from_selected(grammar_list, uv_type_radios):
    global tangle_info
    global selectedObj
    global tangle

    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

    base_grammar = pm.textScrollList(grammar_list, q=True, si=True)[0]
    grammar_filename = None
    # grammar_file_path = pm.workspace.getPath() + "/zentangler/grammars/"
    grammar_file_path = SCRIPT_DIR + "/../zentangler/grammars/"

    if base_grammar == "Style1":
        grammar_filename = grammar_file_path + "test_grammar_1.json"
    if base_grammar == "Style2":
        grammar_filename = grammar_file_path + "test_grammar_1.json"
    if base_grammar == "Style3":
        grammar_filename = grammar_file_path + "test_grammar_1.json"
    if base_grammar == "Style4":
        grammar_filename = grammar_file_path + "test_grammar_1.json"
    elif base_grammar == "Random":      # todo: randomize
        grammar_filename = grammar_file_path + "test_grammar_1.json"

    # make sure we have some objects selected
    selectedObj = pm.ls(sl=True)[0]

    if uv_type_radios.getSelect() == 1:
        tangle_info = create_uv_map_tangle(selectedObj, grammar_filename=grammar_filename)
    elif uv_type_radios.getSelect() == 2:
        tangle_info = create_silhouette_tangle(selectedObj, grammar_filename=grammar_filename)

    tangle = tangle_info.get("tangle")

    # with pm.columnLayout(adjustableColumn=True):
    #     pm.text("1")
    # pm.setParent(window)
    # pm.showWindow(window)

    add_rules_to_ui()


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
    window = pm.window('CreateZenTangleWindow', title="Create ZenTangle", iconName='ZTangler', widthHeight=(400, 400))
    with pm.scrollLayout():
        with pm.columnLayout(adjustableColumn=True):
            pm.text("Select Object(s) to create the tangle")
            # with pm.gridLayout(numberOfColumns=2, cellWidth=100, cellHeight=40):
            pm.text(label="Base Tangle Rules: ", align="left")
            grammar = pm.textScrollList(
                append=["Random", "Style1", "Style2", "Style3", "Style4"],
                selectItem="Random",
                height=80
            )
            pm.text(label="Apply as: ", align="left")
            uv_type = pm.radioButtonGrp(
                labelArray2=["current uv map", "silhouette"],
                numberOfRadioButtons=2,
                select=1
            )
        # cmds.textScrollList( s, q=True, si=True )

        pm.button("Create", command=pm.Callback(create_tangles_from_selected, grammar, uv_type))
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

                   # familyImage = familyImage,
                   # mnemonic = 'alfred',
                   # helpMenu = True,
                   )

    pm.menuItem(l='Create', p=menu, c=pm.Callback(create_tangle_window))

add_zentangler_menu()