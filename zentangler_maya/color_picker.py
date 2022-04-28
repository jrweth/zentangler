import pymel.core as pm
from zentangler_maya.rule_editor import param_value_changed


def open_color_editor(uv_shell_index, rule_index, param_name, tangle, color_index, cbutton):
    """
    open up the built in color editor after clicking on a color button
    Parameters:
        uv_shell_index: int
            index of the uv shell for the tangle
        rule_index: int
            index of the rule in the tangle grammar
        param_name: string
            name of the parameter to which this color belongs
        tangle: Tangle
            the tangle which contains the grammar
        color_index: int
            the list index of the color in the array of colors for this rule (-1 if not multiple)
        colors: list
            the current list of colors for this
        cbutton: button
            the button that was pressed to select the color

    """
    result = pm.colorEditor()
    buffer = result.split()
    if '1' == buffer[3]:
        rgb_value = pm.colorEditor(query=True, rgb=True)
        cbutton.setBackgroundColor(rgb_value)

        # if this is a single color parameter value then set the parameter to the rgb_value
        if color_index == -1:
            param_value_changed(uv_shell_index, rule_index, param_name, tangle, rgb_value)
        # otherwise update the colors array
        else:
            colors = tangle.grammar.rules[rule_index].operator.get_parameter_value(param_name)
            colors[color_index] = rgb_value
            param_value_changed(uv_shell_index, rule_index, param_name, tangle, colors)
    else:
        print('Editor was dismissed')

def color_button(uv_shell_index, rule_index, param_name, tangle, color_index, color, color_layout):
    """
    create a color button
    Parameters:
        uv_shell_index: int
            index of the uv shell
        rule_index:
            index of the rule in the tangle grammar
        param_name:
            name of the parameter that contains the color
        tangle:
            the tangle being manipulated
        color_index:
            the index of the color in the list of colors
        color:
            the current rgb value of the color
        color_layout:
            the parent container of the color button
    """
    # if this is just a single button then just make the button
    if color_index == -1:
        cbutton = pm.button(backgroundColor=color, label="")
        cbutton.command(pm.Callback(open_color_editor,
            uv_shell_index, rule_index, param_name, tangle, color_index, cbutton
        ))
    else:
        #if this is a multiple color button then add a button and a delete color button
        with pm.rowLayout(numberOfColumns=2):
            cbutton = pm.button(backgroundColor=color[color_index], label="")
            cbutton.setCommand(pm.Callback(open_color_editor,
                uv_shell_index, rule_index, param_name, tangle, color_index, cbutton
            ))
            pm.button(label="-", command=pm.Callback( delete_color,
                uv_shell_index, rule_index, param_name, tangle, color_index, color_layout))

def delete_color(uv_shell_index, rule_index, param_name, tangle, color_index, color_layout):
    """
    delete the color from the list of colors
       Parameters:
        uv_shell_index: int
            index of the uv shell
        rule_index:
            index of the rule in the tangle grammar
        param_name:
            name of the parameter that contains the color
        tangle:
            the tangle being manipulated
        color_index:
            the index of the color in the list of colors
        color_layout:
            the parent container of the color button
    """
    colors = tangle.grammar.rules[rule_index].operator.get_parameter_value(param_name)
    if(len(colors) > 1):
        del colors[color_index]
        param_value_changed(uv_shell_index, rule_index, param_name, tangle, colors)
        update_color_buttons(uv_shell_index, rule_index, tangle, param_name, color_layout)

def insert_color(uv_shell_index, rule_index, param_name, tangle, color_layout):
    """
    insert a color into the list of colors
    Parameters:
        uv_shell_index: int
            index of the uv shell
        rule_index:
            index of the rule in the tangle grammar
        param_name:
            name of the parameter that contains the color
        tangle:
            the tangle being manipulated
        color_layout:
            the parent container of the color button
    """
    result = pm.colorEditor()
    buffer = result.split()
    if '1' == buffer[3]:
        rgb_value = pm.colorEditor(query=True, rgb=True)
        # get the current colors and append the new one
        colors = tangle.grammar.rules[rule_index].operator.get_parameter_value(param_name)
        colors.append(rgb_value)
        param_value_changed(uv_shell_index, rule_index, param_name, tangle, colors)
        update_color_buttons(uv_shell_index, rule_index, tangle, param_name, color_layout)

def update_color_buttons(uv_shell_index, rule_index, tangle, param_name, color_layout):
    """
    re initialize all the color buttons for this color list
    Parameters:
        uv_shell_index: int
            index of the uv shell
        rule_index:
            index of the rule in the tangle grammar
        param_name:
            name of the parameter that contains the color
        tangle:
            the tangle being manipulated
        color_layout:
            the parent container of the color button
    """
    # delete all the current buttons
    for child in color_layout.children():
        pm.deleteUI(child)

    # reinitialize the new colors
    with color_layout:
        colors = tangle.grammar.rules[rule_index].operator.get_parameter_value(param_name)
        for color_index in range(len(colors)):
            color_button(uv_shell_index, rule_index, param_name, tangle, color_index, colors, color_layout)
        pm.button(label="+", command=pm.Callback(
            insert_color,
            uv_shell_index,
            rule_index,
            param_name,
            tangle,
            color_layout
        ))