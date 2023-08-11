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
        except (IndexError, KeyError):
            self.logDefaultFilename = "testerNlogger.log"
        try:
            self.logClearFilesOnStart = False
            if self.config['LOG']['CLEAR_ALL_LOG_FILES_ON_START'] == 'True':
                self.logClearFilesOnStart = True
        except (IndexError, KeyError):
            self.logClearFilesOnStart = False
        try:
            self.logRotationMaxBytesSize = int(self.config['LOG']['ROTATION_MAX_BYTES_SIZE'])
        except (IndexError, KeyError):
            self.logRotationMaxBytesSize = 1000000  # 1MB
        try:
            self.logRotationMaxNumberOfFiles = int(self.config['LOG']['ROTATION_MAX_NUMBER_OF_FILES'])
        except (IndexError, KeyError):
            self.logRotationMaxNumberOfFiles = 10
        return self

    def _get_connection_configs(self):
        # Optional
        try:
            self.connInterval = int(self.config['CONNECTION']['INTERVAL_TO_TEST_CONNECTION_IN_SECONDS'])
        except (IndexError, KeyError):
            self.connInterval = 15
        try:
            self.connDNSServerIP = self.config['CONNECTION']['DNS_SERVER_IP']
        except (IndexError, KeyError):
            self.connDNSServerIP = "8.8.8.8"
        try:
            self.conDNSServerPort = int(self.config['CONNECTION']['DNS_SERVER_PORT'])
        except (IndexError, KeyError):
            self.conDNSServerPort = 53
        try:
            self.connTimeOut = int(self.config['CONNECTION']['TIME_OUT'])
        except (IndexError, KeyError):
            self.connTimeOut = 10
        return self

    def _get_notification_configs(self):
        # Optional
        try:
            self.notificationEnabled = False
            if self.config['NOTIFICATION']['ENABLE_NOTIFICATION'] == 'True':
                self.notificationEnabled = True
        except (IndexError, KeyError):
            self.notificationEnabled = False
        # Required
        if self.notificationEnabled:
            self.notificationPhoneNumber = self.config['NOTIFICATION']['PHONE_NUMBER']
            self.notificationApiKey = self.config['NOTIFICATION']['API_KEY']
        else:
            self.notificationPhoneNumber = ''
            self.notificationApiKey = ''
        # Optional
        try:
            self.notificationFakeModeEnabled = False
            if self.config['NOTIFICATION']['ENABLE_FAKE_MODE'] == 'True':
                self.notificationFakeModeEnabled = True
        except (IndexError, KeyError):
            self.notificationFakeModeEnabled = False
        return self
