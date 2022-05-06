import sys

# Imports to use the Maya Python API
import maya.OpenMayaMPx as OpenMayaMPx

from zentangler_maya.maya_menu import add_zentangler_menu, remove_zentangler_menu

# The name of the command.
kPluginCmdName = "addZentanglerMenu"

class addZentanglerMenuCommand(OpenMayaMPx.MPxCommand):
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)

    def doIt(self):
        self.setResult("Executed command")
        add_zentangler_menu()

# Create an instance of the command.
def cmdCreator():
    return OpenMayaMPx.asMPxPtr(addZentanglerMenuCommand())

# Initialize the plugin
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject, "sashireuben@upenn", "1.0", "2022")
    try:
        mplugin.registerCommand(kPluginCmdName, cmdCreator)
        add_zentangler_menu()
    except:
        sys.stderr.write("Failed to register command: %s\n" % kPluginCmdName)
        raise

# Uninitialize the plugin
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterCommand(kPluginCmdName)
        remove_zentangler_menu()
    except:
        sys.stderr.write("Failed to unregister command: %s\n" % kPluginCmdName)
        raise