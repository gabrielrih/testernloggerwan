from unittest import TestCase
from pathlib import Path

from src.libs.logger import start_logger, clear_logs


class TestLogger(TestCase):

    __FOLDER = './log-test/'
    __FILENAME = 'test.log'
    __ROTATION_MAX_BYTES_SIZE = 1000000
    __ROTATION_MAX_NUMBER_OF_FILES = 10

    def test_start_logger(self):
        # Given
        logger = start_logger(self.__FOLDER, \
                              self.__FILENAME, \
                              self.__ROTATION_MAX_BYTES_SIZE, \
                              self.__ROTATION_MAX_NUMBER_OF_FILES)
        # Then
        file = Path(self.__FOLDER + '/' + self.__FILENAME)
        # When
        self.assertEqual(file.exists(), True)
        self.assertIsNotNone(logger)

    def test_clear_logs(self):
        # Given
        clear_logs(self.__FOLDER, self.__FILENAME)
        # Then
        file = Path(self.__FOLDER + '/' + self.__FILENAME)
        # When
        self.assertEqual(file.exists(), False)