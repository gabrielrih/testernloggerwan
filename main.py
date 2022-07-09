# Tester N Logger
# It tests and it logs the wan connection status.
# <gabrielrih>
import time
import sys
import argparse

# Private libraries
from config import read_config
from connection import test_connection
from logger import *
from notification import send_free_notification

def main():

    # Get configs
    configFileName = get_arguments()
    config, error = read_config(configFileName)
    if error:
        sys.exit(error)

    # Start logger and cleaning up if needed
    logDefaultFolder, logDefaultFilename, clearLogFilesOnStart, enableDebugMode = parse_log_configs(config)
    if clearLogFilesOnStart == 'True':
        clear_logs(logDefaultFolder, logDefaultFilename)
    connectionLog = start_logger(logDefaultFolder, logDefaultFilename, enableDebugMode)
    connectionLog.info("Starting TesterNLogger process...")

    # Connection check
    intervalToTest = parse_connection_configs(config)
    enableNotification, phoneNumber, apiKey, enableDebugModeInNotification = parse_notification_configs(config)
    isUpLast = True # Pretends the first connection test was UP
    while (True):
        isUp, errorReason = test_connection()
        connectionLog.debug("Connection status is up? " + str(isUp) + " - Last connection status was up? " + str(isUpLast))
        if isUpLast != isUp: # Internet status was changed
            if isUp:
                connectionLog.warning("Internet connection is UP!")
                if enableNotification == 'True':
                    send_notification(phoneNumber, apiKey, enableDebugModeInNotification, timeWhenItWasDown)
            else:
                timeWhenItWasDown = time.time()
                connectionLog.warning("Internet connection is DOWN! Error: " + errorReason)            
        isUpLast = isUp
        time.sleep(intervalToTest)

def get_arguments():
    parser = argparse.ArgumentParser(description='TesterNLogger WAN connection. It tests the connection and log it every time the connection status changed.')
    parser.add_argument('--config', '-c', help='Configuration file', required=True)
    args = parser.parse_args()
    configFileName = args.config
    return configFileName

def parse_log_configs(config):
    logDefaultFolder = config['LOG']['DEFAULT_FOLDER']
    logDefaultFilename = config['LOG']['DEFAULT_FILENAME']
    clearLogFilesOnStart = config['LOG']['CLEAR_ALL_LOG_FILES_ON_START']
    enableDebugMode = config['LOG']['ENABLE_DEBUG_MODE']
    return logDefaultFolder, logDefaultFilename, clearLogFilesOnStart, enableDebugMode

def parse_connection_configs(config):
    intervalToTest = int(config['CONNECTION']['INTERVAL_TO_TEST_CONNECTION_IN_SECONDS'])
    return intervalToTest

def parse_notification_configs(config):
    enableNotification = config['NOTIFICATION']['ENABLE_NOTIFICATION']
    phoneNumber = config['NOTIFICATION']['PHONE_NUMBER']
    apiKey = config['NOTIFICATION']['API_KEY']
    enableDebugModeInNotification = config['NOTIFICATION']['ENABLE_DEBUG_MODE']
    return enableNotification, phoneNumber, apiKey, enableDebugModeInNotification

def send_notification(phoneNumber, apiKey, enableDebugModeInNotification, timeWhenItWasDown):
    timeNow = time.time()
    downtime = timeWhenItWasDown - timeNow
    message = "TEST: Internet connection was down but now it is UP again. Downtime: " + downtime + " seconds"
    send_free_notification(message, phoneNumber, apiKey, enableDebugModeInNotification)

if __name__ == '__main__':
    main()