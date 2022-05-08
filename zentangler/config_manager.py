import os
import subprocess
import sys
import importlib
import json
import platform

class ConfigManager:

    inkscape_executable: str = None
    config_loaded: bool = False
    config_filename: str = None

    @staticmethod
    def set_config_filename(config_filename: str = None):
        if config_filename is None:
            config_filename = ConfigManager.get_default_config_filename()
        ConfigManager.config_filename = config_filename

    @staticmethod
    def load_config_file(config_filename: str = None):
        ConfigManager.set_config_filename(config_filename)
        if ConfigManager.config_file_exists():
            with open(ConfigManager.get_config_filename()) as jsonfile:
                config = json.load(jsonfile)
                for field in config:
                    if field == "inkscape_executable":
                        ConfigManager.inkscape_executable = config[field]
            ConfigManager.config_loaded = True

    @staticmethod
    def initiate_config_file(config_filename: str = None, inkscape_executable = None):
        ConfigManager.set_config_filename(config_filename)

        if inkscape_executable is None:
            inkscape_executable = ConfigManager.find_default_inkscape_executable()

        config = {"inkscape_executable": inkscape_executable}

        with open(ConfigManager.get_config_filename(), 'w') as outfile:
            json.dump(config, outfile)

    @staticmethod
    def find_default_inkscape_executable():
        if platform.system() == 'Windows':
            default = "/Program Files/Inkscape/bin/inkscape.exe"
            if os.path.exists(default):
                return default
            else:
                return ""
        else:
            try:
                inkscape_path = subprocess.check_output(["which", "inkscape"]).strip()
                return inkscape_path.decode("utf-8")
            except subprocess.CalledProcessError:
                print("ERROR: You need inkscape installed to use this script and specify install location.")
                return ""

    @staticmethod
    def config_file_exists():
        return os.path.exists(ConfigManager.get_config_filename())

    @staticmethod
    def get_inkscape_executable():
        if ConfigManager.config_filename is None:
            ConfigManager.set_config_filename()
        if not ConfigManager.config_loaded:
            ConfigManager.load_config_file()
        return ConfigManager.inkscape_executable


    @staticmethod
    def get_config_filename():
        if ConfigManager.config_filename is None:
            ConfigManager.set_config_filename()
        return ConfigManager.config_filename

    @staticmethod
    def get_default_config_filename():
        SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
        return SCRIPT_DIR + os.path.sep + "config" + os.path.sep + "zentangler_config.json"



    @staticmethod
    def load_dependencies():
        dependencies = ["shapely", "perlin_noise", "pyclipper", "svgwrite"]
        for dep in dependencies:
            if importlib.util.find_spec(dep) is None:
                subprocess.check_call([sys.executable, "-m", "pip", "install", dep])

    @staticmethod
    def set_inkscape_executable(inkscape_executable):
        ConfigManager.inkscape_executable = inkscape_executable

    @staticmethod
    def save_config_file(config_filename: str = None):
        if config_filename is None:
            config_filename = ConfigManager.get_config_filename()

        config = {"inkscape_executable": ConfigManager.inkscape_executable}
        print('saving' + config_filename, config)


        with open(config_filename, 'w') as outfile:
            json.dump(config, outfile)