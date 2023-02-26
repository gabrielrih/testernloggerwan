"""
    Tester N Logger
    It tests and it logs the wan connection status.
    <gabrielrih>
"""
import time
from os.path import exists

# Private libraries
from libs.argument import get_arguments
from libs.connection import *
from libs.logger import *
import libs.config as config
from callmebot import send_free_notification # Module from GitHub

def main():

    # Get configs
    configFileName, debugEnabled = get_arguments()
    if not exists(configFileName):
        raise Exception("ERROR: Config file wasn't found! Check if the config file exists and if it has the right name.")
    configs = config.Config(configFileName)
    configs.get_configs()
    
    # Start logger and cleaning up if needed
    if configs.logClearFilesOnStart == 'True':
        clear_logs(configs.logDefaultFolder, configs.logDefaultFilename)
    connectionLog = start_logger(configs.logDefaultFolder,
                                 configs.logDefaultFilename,
                                 configs.logRotationMaxBytesSize,
                                 configs.logRotationMaxNumberOfFiles,
                                 debugEnabled)
    connectionLog.info("Starting TesterNLogger process...")
    connectionLog.info("Testing the WAN connection every " + str(configs.connInterval) + " seconds.")

    # Connection check
    connectionLog.info("Connection configs: IP " + str(configs.connDNSServerIP) + " Port " + str(configs.conDNSServerPort) + " Timeout " + str(configs.connTimeOut))
    isUpLast = True # Pretends the first connection test was UP
    while (True):
        isUp, errorReason = test_connection_socket(configs.connDNSServerIP, configs.conDNSServerPort, configs.connTimeOut)
        connectionLog.debug("Testing connection... isUp: " + str(isUp) + " isUpLast: " + str(isUpLast))
        if isUpLast == isUp: # Connection status hasn't changed
            time.sleep(configs.connInterval)
            continue
        if isUp:
            timeWhenItTurnsUp = time.time()
            downtime = get_downtime_in_minutes(timeWhenItWasDown, timeWhenItTurnsUp)
            connectionLog.warning("Internet connection is UP! Downtime: " + str(downtime) + ' minute(s)')
            if configs.notificationEnabled == 'True':
                connectionLog.info("Sending notification...")
                wasSent, response = notification(lastErrorReason, downtime, configs.notificationPhoneNumber, configs.notificationApiKey, configs.notificationFakeModeEnabled)
                connectionLog.debug("Notification - It was sent?: " + str(wasSent) + " | Response: " + str(response))
                if wasSent == False:
                    connectionLog.critical("Notification error: " + str(response))
        else: # It's down
            timeWhenItWasDown = time.time()
            lastErrorReason = errorReason
            connectionLog.warning("Internet connection is DOWN! Error: " + errorReason)            
        isUpLast = isUp
        time.sleep(configs.connInterval)

def get_downtime_in_minutes(timeWhenItWasDown, timeWhenItTurnsUp):
    downtime = timeWhenItTurnsUp - timeWhenItWasDown
    return round(downtime / 60, 2)

def notification(lastErrorReason, downtime, phoneNumber, apiKey, fakeModeEnabled):
    customMessage = custom_notification_message(lastErrorReason, downtime)
    wasSent, response = send_free_notification(customMessage, phoneNumber, apiKey, fakeModeEnabled)
    return wasSent, response

def custom_notification_message(errorMessage, downtime):
    errorMessage = str(errorMessage)
    customMessage = "Internet connection was down but now it is UP again. "
    customMessage += "Downtime: " + str(downtime) + ' minute(s).'
    if errorMessage:
        customMessage += "\n"
        customMessage += "Error:" + str(errorMessage)
    return customMessage

if __name__ == '__main__':
    main()