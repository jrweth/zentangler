import pymel.core as pm
from zentangler.operators.split_operator import SplitOperator
from zentangler.operators.outline_operator import OutlineOperator
from zentangler.operators.operator_parameter import OperatorParameterValue as OPV
from zentangler.operators.operator_parameter import ParameterDataType
from zentangler.rule import Rule
from zentangler.tangle import Tangle

"""
import sys
# This should be the path your PyCharm installation
pydevd_egg = r"C:\Program Files\JetBrains\PyCharm 2020.3.3\debug-eggs\pydevd-pycharm.egg"
if not pydevd_egg in sys.path:
    sys.path.append(pydevd_egg)
import pydevd
# This clears out any previous connection in case you restarted the debugger from PyCharm
pydevd.stoptrace()
# 9001 matches the port number that I specified in my configuration
pydevd.settrace('localhost', port=9001, stdoutToServer=True, stderrToServer=True, suspend=False)
"""

icon_images = {"switch": ""}
rules = []


def get_rule_image_filename(object_name, uv_shell_index, rule_index):
    zentangle_path = str(pm.workspace.getPath() + "/zentangler/")
    filename = zentangle_path + "_rule_" + object_name + "_" + str(uv_shell_index) + "_" + str(rule_index) + ".png"
    return filename


def make_operator_icon(rule, object_name, uv_shell_index, rule_index):
    global icon_images
    file_name = get_rule_image_filename(object_name, uv_shell_index, rule_index)
    rule.operator.create_thumbnail(file_name)
    icon_images[file_name].setImage("")
    icon_images[file_name].setImage(file_name)
    pm.refresh()


def param_value_changed(uv_shell_index, rule_index, param_name, tangle, *args):
    parameterValue = OPV(param_name, args[0])
    tangle.update_rule_parameter(rule_index, parameterValue)
    make_operator_icon(tangle.grammar.rules[rule_index], "obj1", uv_shell_index, rule_index)


def add_grammar_rule_widget(uv_shell_index, rule_index, rule: Rule, tangle: Tangle):
    from zentangler_maya.color_picker import color_button, update_color_buttons
    global icon_images
    rules.append(rule)

    with pm.frameLayout(label=rule.name, collapsable=True, collapse=True):
        image_path = get_rule_image_filename("obj1", uv_shell_index, rule_index)
        icon_images[image_path] = pm.image(image=image_path, backgroundColor=[0.5, 0.5, 0.5], width=100, height=100)
        make_operator_icon(rule, "obj1", uv_shell_index, rule_index)
        for param in rule.operator.parameters:
            with pm.rowLayout(numberOfColumns=2, columnWidth2=[100, 100]):
                pm.text(param.name)
                value = rule.operator.get_parameter_value(param.name)

                if param.data_type == ParameterDataType.INT:
                    pm.intSlider(value=value,
                                 changeCommand=pm.CallbackWithArgs(param_value_changed, uv_shell_index, rule_index,
                                                                   param.name, tangle),
                                 min=param.range_start, max=param.range_end, step=1)

                elif param.data_type == ParameterDataType.FLOAT:
                    pm.floatSlider(value=value,
                                   changeCommand=pm.CallbackWithArgs(param_value_changed, uv_shell_index, rule_index,
                                                                     param.name, tangle),
                                   min=param.range_start, max=param.range_end, step=0.01)

                elif param.data_type == ParameterDataType.BOOL:
                    pm.checkBox(value=value, label='',
                                changeCommand=pm.CallbackWithArgs(param_value_changed, uv_shell_index, rule_index,
                                                                  param.name, tangle))

                # if param.data_type == ParameterDataType.STRING and param.name == "line_style":
                #     styles_menu = pm.optionMenu(changeCommand=pm.CallbackWithArgs(param_value_changed, uv_shell_index,
                #                                                                   rule_index, param.name, tangle))
                #     index = 0
                #     for style in LINE_STYLE:
                #         pm.menuItem(label=style)

                elif param.data_type == ParameterDataType.STRING:
                    styles_menu = pm.optionMenu(changeCommand=pm.CallbackWithArgs(param_value_changed, uv_shell_index,
                                                                                  rule_index, param.name, tangle))
                    index = 0
                    for style in param.options:
                        pm.menuItem(label=style)

                elif param.data_type == ParameterDataType.RGB_COLOR:
                    color_layout = pm.columnLayout()
                    if param.is_multiple:
                        update_color_buttons(uv_shell_index, rule_index, tangle, param.name, color_layout)
                    else:
                        color_button(uv_shell_index, rule_index, param.name, tangle, -1, value, color_layout)
                    # for style in LINE_STYLE:
                    #     index += 1
                    #     if style == value:
                    #         pm.optionMenu(styles_menu, select=index)

                    # pm.optionMenu(styles_menu, value=value)

                # if param.data_type == ParameterDataType.STRING:
                #     pm.textField(text=value,
                #                  changeCommand=pm.CallbackWithArgs(param_value_changed, uv_shell_index, rule_index,
                #                                                    param.name))


# Make a new window
def OpenZentangler():
    global rule1
    global rule2
    window = pm.window(title="ZenTangler", iconName='ZTangler', widthHeight=(200, 200))
    with pm.scrollLayout():
        with pm.columnLayout(adjustableColumn=True):
            pm.text("Tangle Grammar Editor")
            add_grammar_rule_widget(0, 0, rule1)
            add_grammar_rule_widget(0, 1, rule2)
    # Result: ui.Button('window1|columnLayout98|button112') #
    pm.setParent('..')
    # Result: u'' #
    pm.showWindow(window)

# OpenZentangler()
