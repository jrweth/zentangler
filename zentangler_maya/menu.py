import pymel.core as pm
from zentangler_maya.tangle_creation import create_uv_map_tangle, create_silhouette_tangle

def create_tangles_from_selected(grammar_list, uv_type_radios):
    base_grammar = pm.textScrollList(grammar_list, q=True, si=True)[0]
    if base_grammar == "Style1":
        grammar_filename = "style1 filename"
    elif base_grammar == "Random":
        grammar_filename = "random filename"

    # make sure we have some objects selected
    selected = pm.ls(sl=True)[0]

    if uv_type_radios.getSelect() == 1:
        tangle_info = create_uv_map_tangle(object=selected, grammar_filename=grammar_filename)
    elif uv_type_radios.getSelect() == 2:
        tangle_info = create_silhouette_tangle(object=selected, grammar_filename=grammar_filename)


def create_tangle_window():
    # if the window already exists then delete it
    if pm.window('CreateZenTangleWindow', exists=True):
        pm.deleteUI("CreateZenTangleWindow")

    window = pm.window('CreateZenTangleWindow', title="Create ZenTangle", iconName='ZTangler', widthHeight=(400, 400))
    with pm.scrollLayout():
        with pm.columnLayout(adjustableColumn=True):
            pm.text("Select Object(s) to create the tangle")
            with pm.gridLayout(numberOfColumns=2, cellWidth=100, cellHeight=40):
                pm.text("Base Tangle Rules")
            grammar = pm.textScrollList(
                append=["Random", "Style1", "Style2", "Style3", "Style4"],
                selectItem="Random"
            )
        uv_type = pm.radioButtonGrp(
            label="apply to",
            labelArray2=["current uv map", "silhouette"],
            numberOfRadioButtons=2,
            select=1
        )
        # cmds.textScrollList( s, q=True, si=True )

        pm.button("create", command=pm.Callback(create_tangles_from_selected, grammar, uv_type))
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

