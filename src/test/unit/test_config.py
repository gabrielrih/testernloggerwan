from unittest import TestCase

from src.libs.config import Config


class TestConfig(TestCase):

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
        self.assertEqual(configs.logClearFilesOnStart, str(False))
        self.assertEqual(configs.logRotationMaxBytesSize, 1000000)
        self.assertEqual(configs.logRotationMaxNumberOfFiles, 10)

    def test_check_notification_configs(self):
        # Given
        cf = Config(self.__CONFIG_FILE)
        # Then
        configs = cf.get_configs()
        # When
        self.assertEqual(configs.notificationEnabled, str(False))
        self.assertEqual(configs.notificationFakeModeEnabled, str(False))
        self.assertEqual(configs.notificationPhoneNumber, '') #  Empty when disabled
        self.assertEqual(configs.notificationApiKey, '') #  Empty when disabled
