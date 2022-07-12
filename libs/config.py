"""
    Class for get the configurations based on a file.
    It returns an error if the file doesn't exist or if it doesn't have the required configurations.
    Reference: https://docs.python.org/3/library/configparser.html
    <gabrielrih>
"""
import configparser

class Config:
    def __init__(self, path):
        self.path = path

    def get_configs(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.path)
        self._get_log_configs()
        self._get_connection_configs()
        self._get_notification_configs()
        return self

    def _get_log_configs(self):
        # Required
        self.logDefaultFolder = self.config['LOG']['DEFAULT_FOLDER']
        # Optional
        try:
            self.logDefaultFilename = self.config['LOG']['DEFAULT_FILENAME']
        except:
            self.logDefaultFilename = "testerNlogger.log"
        try:
            self.logClearFilesOnStart = self.config['LOG']['CLEAR_ALL_LOG_FILES_ON_START']
        except:
            self.logClearFilesOnStart = False
        return self

    def _get_connection_configs(self):
        # Optional
        try:
            self.connInterval = int(self.config['CONNECTION']['INTERVAL_TO_TEST_CONNECTION_IN_SECONDS'])
        except:
            self.connInterval = 15
        try:
            self.connDNSServerIP = self.config['CONNECTION']['DNS_SERVER_IP']
        except:
            self.connDNSServerIP = "8.8.8.8"
        try:
            self.conDNSServerPort = int(self.config['CONNECTION']['DNS_SERVER_PORT'])
        except:
            self.conDNSServerPort = 53
        try:
            self.connTimeOut = int(self.config['CONNECTION']['TIME_OUT'])
        except:
            self.connTimeOut = 10
        return self

    def _get_notification_configs(self):
        # Optional
        try:
            self.notificationEnabled = self.config['NOTIFICATION']['ENABLE_NOTIFICATION']
        except:
            self.notificationEnabled = False
        # Required
        if self.notificationEnabled == 'True':
            self.notificationPhoneNumber = self.config['NOTIFICATION']['PHONE_NUMBER']
            self.notificationApiKey = self.config['NOTIFICATION']['API_KEY']

        else:
            self.notificationPhoneNumber = ''
            self.notificationApiKey = ''
        # Optional
        try:
            self.notificationFakeModeEnabled = self.config['NOTIFICATION']['ENABLE_FAKE_MODE']
        except:
            self.notificationFakeModeEnabled = False
        return self