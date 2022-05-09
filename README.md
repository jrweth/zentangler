#Zentangler Maya Plugin#
A maya plugin for creating procedurally generated textures based upon 
predefined shape grammars

## Requirements
* Maya version 2022 and after (with PyMel install option)
* Inkscape version 1.1.2 and after (for SVG to PNG conversion)

##Installation Instructions

###Install Python dependencies in Maya Python environment
There are several python dependencies that must be installed in the maya python environment.  The *mayapy* executable is found in the bin directory of the Maya2022 application folder. See [Managing Python packages with mayapy and pip](https://knowledge.autodesk.com/support/maya/learn-explore/caas/CloudHelp/cloudhelp/2022/ENU/Maya-Scripting/files/GUID-72A245EC-CDB4-46AB-BEE0-4BBBF9791627-htm.html) Navigate to the folder with your terminal application and run the following:
* mayapy -m pip install shapely
* mayapy -m pip install svgwrite
* mayapy -m pip install perlin-noise
* mayapy -m pip install pyclipper

###Copy Plugin file to plugin folder
Copy the *zentangler_plugin.py* file to a folder where Maya is configured to keep plugins.  See [Autodesk Article](https://knowledge.autodesk.com/support/maya/learn-explore/caas/CloudHelp/cloudhelp/2022/ENU/Maya-Customizing/files/GUID-FA51BD26-86F3-4F41-9486-2C3CF52B9E17-htm.html)

###Copy Python code files to maya python script folder
Copy the *zentangler* and *zentangler_maya* folders to the script folder which is included in maya's Python path [Maya File Path Variables](https://knowledge.autodesk.com/support/maya/learn-explore/caas/CloudHelp/cloudhelp/2022/ENU/Maya-EnvVar/files/GUID-228CCA33-4AFE-4380-8C3D-18D23F7EAC72-htm.html)


###Install Inkscape
Zentangler uses Inkscape to convert SVG files into PNG files, this needs to be installed in order for zentanger to produce textures usable by Maya.

###Load the ZenTangler plugin
Open up maya and then use Maya's Plugin-Manager to load the ZenTangler plugin which was copied to Maya's plugin folder.  This should add a ZenTangler menu item.

###Configure Zentangler to use the Inkscape executable
Once the plugin is loaded use the ZentanglerMenu>Set Configuration option and enter in the Inkscape executable file for your system.  Depending on your platform and how Inkscape was installed this may vary.  A likely spot for windows is *"/Program Files/Inkscape/bin/inkscape.exe"* .  Mac OS could be *"/opt/local/bin/inkscape"* or similar.  Once the path is entered click the "save configuration button."
