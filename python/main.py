# Tester N Logger
# It tests and it logs the wan connection status.
# <gabrielrih>
import time

# Private libraries
from config import read_config
from connection import test_connection
from logger import *


def main():
    config = read_config()

    # Start logger and cleaning up if needed
    logDefaultFolder, logDefaultFilename, clearLogFilesOnStart, enableDebugMode = parse_log_configs(config)
    if clearLogFilesOnStart == 'True':
        clear_logs(logDefaultFolder, logDefaultFilename)
    connectionLog = start_logger(logDefaultFolder, logDefaultFilename, enableDebugMode)
    connectionLog.info("Starting TesterNLogger process...")

    # Connection check
    intervalToTest = parse_connection_configs(config)
    isUpLast = True # Pretends the first connection test was UP
    while (True):
        isUp, errorReason = test_connection()
        connectionLog.debug("Connection status is up? " + str(isUp) + " - Last connection status was up? " + str(isUpLast))
        if isUpLast != isUp: # Internet status was changed
            if isUp:
                connectionLog.warning("Internet connection is UP!")
            else:
                connectionLog.warning("Internet connection is DOWN! Error: " + errorReason)            
        isUpLast = isUp

        # Delay for the next connection check
        time.sleep(intervalToTest)


def parse_log_configs(config):
    logDefaultFolder = config['LOG']['DEFAULT_FOLDER']
    logDefaultFilename = config['LOG']['DEFAULT_FILENAME']
    clearLogFilesOnStart = config['LOG']['CLEAR_ALL_LOG_FILES_ON_START']
    enableDebugMode = config['LOG']['ENABLE_DEBUG_MODE']
    return logDefaultFolder, logDefaultFilename, clearLogFilesOnStart, enableDebugMode


def parse_connection_configs(config):
    intervalToTest = int(config['CONNECTION']['INTERVAL_TO_TEST_CONNECTION_IN_SECONDS'])
    return intervalToTest


if __name__ == '__main__':
    main()