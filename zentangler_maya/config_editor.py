import pymel.core as pm
from zentangler.config_manager import ConfigManager

class ConfigEditor:


    def __init__(self):
        if pm.window('ZenTangleConfigWindow', exists=True):
            pm.deleteUI("ZenTangleConfigWindow")
        self.window = pm.window('ZenTangleConfigWindow',
                                title="Config ZenTangler",
                                widthHeight=(400, 100))

        if not ConfigManager.config_file_exists():
            ConfigManager.initiate_config_file()

        inkscape_file = ConfigManager.get_inkscape_executable()
        with pm.columnLayout():

            pm.text("inkscape executable")
            ie_row = pm.rowLayout(numberOfColumns=2)
            ie_row.columnWidth([1, 350])
            ie_row.columnWidth([2, 50])
            with ie_row:
                self.inkscape_executable = pm.textField("inkscape executable", width=350, text=inkscape_file)
                pm.button("find", command=pm.Callback(self.open_inkscape_executable_file_browser))
            pm.button("save configuration", command=pm.Callback(ConfigEditor.save_configuration, self))

        pm.showWindow(self.window)

    def open_inkscape_executable_file_browser(self):
        picker = pm.fileDialog2( hne=True, fileMode=1)
        if picker:
            self.inkscape_executable.setText(picker[0])
        else:
            print("user cancelled")

    def save_configuration(self):
        value = self.inkscape_executable.getFileName()
        ConfigManager.set_inkscape_executable(value)
        ConfigManager.save_config_file()
