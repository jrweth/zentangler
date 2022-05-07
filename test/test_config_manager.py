import unittest
import sys
import os
from zentangler.config_manager import ConfigManager

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR) + '/zentangler')
sys.path.append(os.path.dirname(SCRIPT_DIR))

class TestConfigManager(unittest.TestCase):
    def test_load_dependencies(self):
        ConfigManager.load_dependencies()

    def test_get_default_filename(self):
        filename = ConfigManager.get_default_config_filename()
        print (filename)

    def test_initiate_config_file(self):
        ConfigManager.initiate_config_file()

    def test_get_config_filename(self):
        print(ConfigManager.get_config_filename())
