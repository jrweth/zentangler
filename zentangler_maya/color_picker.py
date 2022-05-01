import pymel.core as pm
from zentangler.operators.operator_parameter import OperatorParameter
from zentangler.rule import Rule

class ColorPicker:
    def __init__(self, rule_editor, container_layout, param: OperatorParameter):
        self.rule_editor = rule_editor
        self.rule: Rule = rule_editor.rule
        self.param = param
        self.container_layout = container_layout
        self.color_buttons = []
        self.operator = rule_editor.operator
        self.create_color_buttons()
        self.current_colors = self.rule.get_parameter_value(self.param.name)

    def create_color_buttons(self):
        # clear the children first
        self.current_colors = self.rule.get_parameter_value(self.param.name)
        for child in self.container_layout.children():
            pm.deleteUI(child)

        with self.container_layout:
            if not self.param.is_multiple:
                self.create_button(-1, self.current_colors)
            else:
                for i in range(len(self.current_colors)):
                    self.create_button(i, self.current_colors[i])
                pm.button(label="+", command=pm.Callback(ColorPicker.insert_color, self))

    def open_color_editor(self, color_index, *args):
        result = pm.colorEditor()
        buffer = result.split()
        if '1' == buffer[3]:
            rgb_value = pm.colorEditor(query=True, rgb=True)

            # if this is a single color parameter value then set the parameter to the rgb_value
            if color_index == -1:
                self.rule_editor.param_value_changed(self.param.name, rgb_value)
            # otherwise update the colors array
            else:
                if color_index == len(self.current_colors):
                    self.current_colors.append(rgb_value)
                else:
                    self.current_colors[color_index] = rgb_value
                self.rule_editor.param_value_changed(self.param.name, self.current_colors)
            #reinitialize the buttons
            self.create_color_buttons()
        else:
            print('Editor was dismissed')

    def insert_color(self):
        colors = self.rule.get_parameter_value(self.param.name)
        self.open_color_editor(len(colors))

    def delete_color(self, color_index, *args):
        # get the existing colors
        colors = self.rule.get_parameter_value(self.param.name)
        new_colors = []
        for i in range(len(colors)):
            if not i == color_index:
                new_colors.append(colors[i])
        self.rule_editor.param_value_changed(self.param.name, new_colors)
        self.create_color_buttons()


    def create_button(self, color_index, rgb_color):
        # for when there is only one color
        if color_index == -1:
            cbutton = pm.button(backgroundColor=rgb_color, label="")
            cbutton.command(pm.Callback(ColorPicker.open_color_editor, self, color_index))
        else:
            # if this is a multiple color button then add a button and a delete color button
            with pm.rowLayout(numberOfColumns=2):
                cbutton = pm.button(backgroundColor=rgb_color, label="")
                cbutton.setCommand(pm.Callback(ColorPicker.open_color_editor, self, color_index))
                if color_index > 0 or len(self.current_colors) > 1:
                    pm.button(label="-", command=pm.Callback(ColorPicker.delete_color, self, color_index))

