import sys

from unittest import TestCase

from src.libs.argument import get_arguments


class TestArguments(TestCase):

    __CONFIG_FILE = "./config/config-example.ini"

    def test_get_arguments(self):
        # Given (Emulates the parameters)
        sys.argv.append('--config')
        sys.argv.append(self.__CONFIG_FILE)
        # When
        config_filename, debug_enabled = get_arguments()
        # Then
        self.assertEqual(config_filename, self.__CONFIG_FILE)
        self.assertFalse(debug_enabled)

    def test_get_arguments_with_debug(self):
        # Given (Emulates the parameters)
        sys.argv.append('--config')
        sys.argv.append(self.__CONFIG_FILE)
        sys.argv.append('--debug')
        # When
        config_filename, debug_enabled = get_arguments()
        # Then
        self.assertEqual(config_filename, self.__CONFIG_FILE)
        self.assertTrue(debug_enabled)
