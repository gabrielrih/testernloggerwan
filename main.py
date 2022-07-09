# Tester N Logger
# It tests and it logs the wan connection status.
# <gabrielrih>
import time
import sys

# Private libraries
from argument import get_arguments
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
        if isUpLast != isUp: # Internet status was changed
            if isUp:
                timeWhenItTurnsUp = time.time()
                connectionLog.warning("Internet connection is UP!")
                if enableNotification == 'True':
                    connectionLog.info("Sending notification!")
                    customMessage = custom_notification_message(lastErrorReason, timeWhenItWasDown, timeWhenItTurnsUp)
                    wasSent, response = send_free_notification(customMessage, phoneNumber, apiKey, enableDebugModeInNotification)
                    connectionLog.debug("Notification - It was sent?: " + str(wasSent) + " | Response: " + str(response))
                    if wasSent == 'False':
                        connectionLog.critical("Sending notification error: " + str(response))
            else:
                timeWhenItWasDown = time.time()
                lastErrorReason = errorReason
                connectionLog.warning("Internet connection is DOWN! Error: " + errorReason)            
        isUpLast = isUp
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


def parse_notification_configs(config):
    enableNotification = config['NOTIFICATION']['ENABLE_NOTIFICATION']
    phoneNumber = config['NOTIFICATION']['PHONE_NUMBER']
    apiKey = config['NOTIFICATION']['API_KEY']
    enableDebugModeInNotification = config['NOTIFICATION']['ENABLE_DEBUG_MODE']
    return enableNotification, phoneNumber, apiKey, enableDebugModeInNotification


def custom_notification_message(errorMessage, timeWhenItWasDown, timeWhenItTurnsUp):
    errorMessage = str(errorMessage)
    downtime = timeWhenItTurnsUp - timeWhenItWasDown
    customMessage = "TEST: "
    customMessage += "Internet connection was down but now it is UP again. "
    customMessage += "Downtime: " + str(downtime) + " seconds. "
    if errorMessage:
        customMessage += "\n"
        customMessage += "Error:" + str(errorMessage)
    return customMessage


if __name__ == '__main__':
    main()