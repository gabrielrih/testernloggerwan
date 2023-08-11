import os

from unittest import TestCase

from src.libs.config import Config



class TestConfigAllConfigs(TestCase):
    ''' Testing the config file when all configurations are present on the file '''

    __CONFIG_FILE = "./config/config-example.ini"

    def test_check_connection_configs(self):
        # Given
        cf = Config(self.__CONFIG_FILE)
        # Then
        configs = cf.get_configs()
        # When
        self.assertEqual(configs.connInterval, 15)
        self.assertEqual(configs.connTimeOut, 10)
        self.assertEqual(configs.connDNSServerIP, '8.8.8.8')
        self.assertEqual(configs.conDNSServerPort, 53)

    def test_check_log_configs(self):
        # Given
        cf = Config(self.__CONFIG_FILE)
        # Then
        configs = cf.get_configs()
        # When
        self.assertEqual(configs.logDefaultFolder, '/var/log/testerNlogger/')
        self.assertEqual(configs.logDefaultFilename, 'testerNlogger.log')
        self.assertEqual(configs.logClearFilesOnStart, False)
        self.assertEqual(configs.logRotationMaxBytesSize, 1000000)
        self.assertEqual(configs.logRotationMaxNumberOfFiles, 10)

    def test_check_notification_configs(self):
        # Given
        cf = Config(self.__CONFIG_FILE)
        # Then
        configs = cf.get_configs()
        # When
        self.assertEqual(configs.notificationEnabled, False)
        self.assertEqual(configs.notificationFakeModeEnabled, False)
        self.assertEqual(configs.notificationPhoneNumber, '')  # Empty when disabled
        self.assertEqual(configs.notificationApiKey, '')  # Empty when disabled


class SetUpClass(TestCase):
    def setUp(self):
        self.setUp()

    def tearDown(self):
        self.tearDown()

class TestOnlyRequiredConfigs(SetUpClass):
    ''' Testing the config file when just the required configurations are set '''

    __CONFIG_FILE = "./config/config-test.ini"

    def setUp(self):
        with open(self.__CONFIG_FILE, 'w') as fp:
            fp.write('')
            fp.write('[LOG]')
            fp.write('\nDEFAULT_FOLDER = /var/log/testerNlogger/')

    def tearDown(self):
        os.remove(self.__CONFIG_FILE)

    def test_check_default_connection_configs(self):
        # Given
        cf = Config(self.__CONFIG_FILE)
        # When
        configs = cf.get_configs()
        # Then
        self.assertEqual(configs.connInterval, 15)
        self.assertEqual(configs.connTimeOut, 10)
        self.assertEqual(configs.connDNSServerIP, '8.8.8.8')
        self.assertEqual(configs.conDNSServerPort, 53)

    def test_check_default_log_configs(self):
        # Given
        cf = Config(self.__CONFIG_FILE)
        # Then
        configs = cf.get_configs()
        # When
        self.assertEqual(configs.logDefaultFolder, '/var/log/testerNlogger/')
        self.assertEqual(configs.logDefaultFilename, 'testerNlogger.log')
        self.assertEqual(configs.logClearFilesOnStart, False)
        self.assertEqual(configs.logRotationMaxBytesSize, 1000000)
        self.assertEqual(configs.logRotationMaxNumberOfFiles, 10)

    def test_check_default_notification_configs(self):
        # Given
        cf = Config(self.__CONFIG_FILE)
        # Then
        configs = cf.get_configs()
        # When
        self.assertEqual(configs.notificationEnabled, False)
        self.assertEqual(configs.notificationFakeModeEnabled, False)
        self.assertEqual(configs.notificationPhoneNumber, '')  # Empty when disabled
        self.assertEqual(configs.notificationApiKey, '')  # Empty when disabled
