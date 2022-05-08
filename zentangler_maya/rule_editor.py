import os
import pymel.core as pm
from zentangler.operators.operator_parameter import OperatorParameterValue as OPV
from zentangler.operators.operator_parameter import ParameterDataType
from zentangler_maya.color_picker import ColorPicker

class RuleEditor:
    def __init__(self, tangle_editor, rule_index):
        self.tangle_editor = tangle_editor
        self.rule_index = rule_index
        self.tangle = self.tangle_editor.tangle
        self.rule = self.tangle.grammar.rules[rule_index]
        self.operator = self.rule.operator
        self.rules_container = self.tangle_editor.rules_container
        self.container = None
        self.initialized = False
        self.icon_image = None
        with self.rules_container:
            self.container = pm.frameLayout(
                label=self.rule.name,
                collapsable=True,
                collapse=True,
                width=375,
                expandCommand=pm.Callback(RuleEditor.on_expand, self)
            )
    def on_expand(self):
        if not self.initialized:
            with self.container:
                filename = self.get_thumbnail_filename()
                self.operator.create_thumbnail(filename)
                self.icon_image = pm.image(image=filename, backgroundColor = [0.5, 0.5, 0.5], width = 100, height = 100)
                for param in self.operator.parameters:
                    self.add_parameter_control(param)
        self.initialized = True

    def param_value_changed(self, param_name, *args):
        param_value = args[0]

        if param_name == "output_tags":
            param_value = param_value[param_value.find("[") + 1:param_value.find("]")]
            param_value = param_value.replace(" ", "").replace("\"", "").replace("\'", "")
            param_value = list(param_value.split(","))

        parameter_value = OPV(param_name, param_value)
        self.tangle.update_rule_parameter(self.rule_index, parameter_value)

        #update the operator icon
        self.operator.create_thumbnail(self.get_thumbnail_filename())
        self.icon_image.setImage(self.get_thumbnail_filename())

    def add_parameter_control(self, param):
        with pm.rowLayout(numberOfColumns=2, columnWidth2=[150, 225]):
            pm.text(param.name)
            value = self.operator.get_parameter_value(param.name)

            if param.data_type == ParameterDataType.INT:
                pm.intSlider(value=value,
                             changeCommand=pm.CallbackWithArgs(RuleEditor.param_value_changed, self, param.name),
                             min=param.range_start, max=param.range_end, step=1)

            elif param.data_type == ParameterDataType.FLOAT:
                pm.floatSlider(value=value,
                               changeCommand=pm.CallbackWithArgs(RuleEditor.param_value_changed, self, param.name),
                               min=param.range_start, max=param.range_end, step=0.01)

            elif param.data_type == ParameterDataType.BOOL:
                pm.checkBox(value=value, label='',
                            changeCommand=pm.CallbackWithArgs(RuleEditor.param_value_changed, self, param.name))

            # if param.data_type == ParameterDataType.STRING and param.name == "line_style":
            #     styles_menu = pm.optionMenu(changeCommand=pm.CallbackWithArgs(param_value_changed, uv_shell_index,
            #                                                                   rule_index, param.name, tangle))
            #     index = 0
            #     for style in LINE_STYLE:
            #         pm.menuItem(label=style)

            elif param.data_type == ParameterDataType.STRING:
                styles_menu = pm.optionMenu(changeCommand=pm.CallbackWithArgs(RuleEditor.param_value_changed, self, param.name))

                index = 0
                for style in param.options:
                    pm.menuItem(label=style)

                try:
                    pm.optionMenu(styles_menu, edit=True, value=value)
                except:
                    print("value " + value + " for " + param.name + " not found")

            elif param.data_type == ParameterDataType.RGB_COLOR:
                color_layout = pm.columnLayout()
                ColorPicker(self, color_layout, param)
                # for style in LINE_STYLE:
                #     index += 1
                #     if style == value:
                #         pm.optionMenu(styles_menu, select=index)

                # pm.optionMenu(styles_menu, value=value)

            elif param.data_type == ParameterDataType.LIST:
                text_str = "[" + ', '.join(f'"{v}"' for v in value) + "]"
                pm.textField(text=text_str,
                             changeCommand=pm.CallbackWithArgs(RuleEditor.param_value_changed, self, param.name))

    def get_thumbnail_filename(self):
        return self.tangle_editor.get_img_folder() + os.path.sep + "rule_" + str(self.rule_index) + "thumbnail.png"

