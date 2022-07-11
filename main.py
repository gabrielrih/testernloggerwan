# Tester N Logger
# It tests and it logs the wan connection status.
# <gabrielrih>
import time
import sys

# Private libraries
from argument import get_arguments
from config import read_config
from connection import *
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
    intervalForTesting, dnsServerIP, dnsServerPort, connectionTimeOut = parse_connection_configs(config)
    connectionLog.debug("DNS Server: " + str(dnsServerIP) + ":" + str(dnsServerPort) + " Connection time out: " + str(connectionTimeOut))
    enableNotification, phoneNumber, apiKey, enableDebugModeInNotification = parse_notification_configs(config)
    isUpLast = True # Pretends the first connection test was UP
    while (True):
        isUp, errorReason = test_connection_socket(dnsServerIP, dnsServerPort, connectionTimeOut)
        if isUpLast != isUp: # Internet status was changed
            if isUp:
                timeWhenItTurnsUp = time.time()
                downtime, unit = get_downtime(timeWhenItWasDown, timeWhenItTurnsUp)
                connectionLog.warning("Internet connection is UP! Downtime: " + str(downtime) + ' ' + unit + '.')
                if enableNotification == 'True':
                    connectionLog.info("Sending notification!")
                    customMessage = custom_notification_message(lastErrorReason, downtime, unit)
                    wasSent, response = send_free_notification(customMessage, phoneNumber, apiKey, enableDebugModeInNotification)
                    connectionLog.debug("Notification - It was sent?: " + str(wasSent) + " | Response: " + str(response))
                    if wasSent == 'False':
                        connectionLog.critical("Sending notification error: " + str(response))
            else:
                timeWhenItWasDown = time.time()
                lastErrorReason = errorReason
                connectionLog.warning("Internet connection is DOWN! Error: " + errorReason)            
        isUpLast = isUp
        time.sleep(intervalForTesting)


def parse_log_configs(config):
    logDefaultFolder = config['LOG']['DEFAULT_FOLDER']
    logDefaultFilename = config['LOG']['DEFAULT_FILENAME']
    clearLogFilesOnStart = config['LOG']['CLEAR_ALL_LOG_FILES_ON_START']
    enableDebugMode = config['LOG']['ENABLE_DEBUG_MODE']
    return logDefaultFolder, logDefaultFilename, clearLogFilesOnStart, enableDebugMode


def parse_connection_configs(config):
    intervalForTesting = int(config['CONNECTION']['INTERVAL_TO_TEST_CONNECTION_IN_SECONDS'])
    dnsServerIP = config['CONNECTION']['DNS_SERVER_IP']
    dnsServerPort = int(config['CONNECTION']['DNS_SERVER_PORT'])
    connectionTimeOut = int(config['CONNECTION']['TIME_OUT'])
    return intervalForTesting, dnsServerIP, dnsServerPort, connectionTimeOut


def parse_notification_configs(config):
    enableNotification = config['NOTIFICATION']['ENABLE_NOTIFICATION']
    phoneNumber = config['NOTIFICATION']['PHONE_NUMBER']
    apiKey = config['NOTIFICATION']['API_KEY']
    enableDebugModeInNotification = config['NOTIFICATION']['ENABLE_DEBUG_MODE']
    return enableNotification, phoneNumber, apiKey, enableDebugModeInNotification


"""
    Returns downtime rounded in two decimals.
    Plus, it returns the unit of measure (seconds, minutes or hours)
"""
def get_downtime(timeWhenItWasDown, timeWhenItTurnsUp):
    downtime = timeWhenItTurnsUp - timeWhenItWasDown
    if downtime >= 3600:
        downtime = downtime / 60 / 60 # Seconds to hours
        unit = 'hours'
    elif downtime >= 60:
        downtime = downtime / 60 # Seconds to minutes
        unit = 'minutes'
    else:
        unit = 'seconds'
    return round(downtime, 2), unit


def custom_notification_message(errorMessage, downtime, unit):
    errorMessage = str(errorMessage)
    customMessage = "TEST: "
    customMessage += "Internet connection was down but now it is UP again. "
    customMessage += "Downtime: " + str(downtime) + ' ' + unit + '.'
    if errorMessage:
        customMessage += "\n"
        customMessage += "Error:" + str(errorMessage)
    return customMessage


if __name__ == '__main__':
    main()