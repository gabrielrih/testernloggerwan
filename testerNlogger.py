"""
    Tester N Logger
    It tests and it logs the wan connection status.
    <gabrielrih>
"""
import time
from os.path import exists

import src.libs.config as config
from src.libs.argument import get_arguments
from src.libs.connection import test_connection_socket
from src.libs.logger import start_logger, clear_logs
from src.libs.notification import SMSNotification
from src.libs.util import get_downtime_in_minutes, custom_notification_message


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
    connectionLog.info("Connection configs: IP " + str(configs.connDNSServerIP) + \
                        " Port " + str(configs.conDNSServerPort) + \
                        " Timeout " + str(configs.connTimeOut))
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
                notification = SMSNotification(configs.notificationApiKey)
                customMessage = custom_notification_message(lastErrorReason, downtime)
                wasSent, response = notification.send_notification(customMessage, configs.notificationPhoneNumber)
                connectionLog.debug("Notification - It was sent?: " + str(wasSent) + " | Response: " + str(response))
                if wasSent == False:
                    connectionLog.critical("Notification error: " + str(response))
        else: # It's down
            timeWhenItWasDown = time.time()
            lastErrorReason = errorReason
            connectionLog.warning("Internet connection is DOWN! Error: " + errorReason)
        isUpLast = isUp
        time.sleep(configs.connInterval)


if __name__ == '__main__':
    main()
