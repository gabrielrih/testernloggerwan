"""
    Tester N Logger
    It tests and it logs the wan connection status.
    <gabrielrih>
"""
import time
from os.path import exists

# Private libraries
from libs.argument import get_arguments
import libs.config as config
from libs.connection import *
from libs.logger import *
from libs.notification import send_free_notification

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
    connectionLog = start_logger(configs.logDefaultFolder, configs.logDefaultFilename, debugEnabled)
    connectionLog.info("Starting TesterNLogger process...")
    connectionLog.info("Testing the WAN connection every " + str(configs.connInterval) + " seconds.")

    # Connection check
    connectionLog.info("Connection configs: IP " + str(configs.connDNSServerIP) + " Port " + str(configs.conDNSServerPort) + " Timeout " + str(configs.connTimeOut))
    isUpLast = True # Pretends the first connection test was UP
    while (True):
        isUp, errorReason = test_connection_socket(configs.connDNSServerIP, configs.conDNSServerPort, configs.connTimeOut)
        connectionLog.debug("Testing connection! isUp: " + str(isUp) + " isUpLast: " + str(isUpLast))
        if isUpLast != isUp: # Internet status was changed
            if isUp:
                timeWhenItTurnsUp = time.time()
                downtime, unit = get_downtime(timeWhenItWasDown, timeWhenItTurnsUp)
                connectionLog.warning("Internet connection is UP! Downtime: " + str(downtime) + ' ' + unit + '.')
                if configs.notificationEnabled == 'True':
                    connectionLog.info("Sending notification!")
                    customMessage = custom_notification_message(lastErrorReason, downtime, unit)
                    wasSent, response = send_free_notification(customMessage, configs.notificationPhoneNumber, configs.notificationApiKey, configs.notificationFakeModeEnabled)
                    connectionLog.debug("Notification - It was sent?: " + str(wasSent) + " | Response: " + str(response))
                    if wasSent == 'False':
                        connectionLog.critical("Sending notification error: " + str(response))
            else:
                timeWhenItWasDown = time.time()
                lastErrorReason = errorReason
                connectionLog.warning("Internet connection is DOWN! Error: " + errorReason)            
        isUpLast = isUp
        time.sleep(configs.connInterval)

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
    customMessage = "Internet connection was down but now it is UP again. "
    customMessage += "Downtime: " + str(downtime) + ' ' + unit + '.'
    if errorMessage:
        customMessage += "\n"
        customMessage += "Error:" + str(errorMessage)
    return customMessage

if __name__ == '__main__':
    main()