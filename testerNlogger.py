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
    config_filename, debug_enabled = get_arguments()
    if not exists(config_filename):
        raise Exception("ERROR: Config file wasn't found! Check if the config file exists and if it has the right name.")
    configs = config.Config(config_filename)
    configs.get_configs()

    # Start logger and cleaning up if needed
    if configs.logClearFilesOnStart == 'True':
        clear_logs(configs.logDefaultFolder, configs.logDefaultFilename)
    connectionLog = start_logger(configs.logDefaultFolder,
                                 configs.logDefaultFilename,
                                 configs.logRotationMaxBytesSize,
                                 configs.logRotationMaxNumberOfFiles,
                                 debug_enabled)
    connectionLog.info("Starting TesterNLogger process...")
    connectionLog.info("Testing the WAN connection every " + str(configs.connInterval) + " seconds.")

    # Connection check
    connectionLog.info("Connection configs: IP " + str(configs.connDNSServerIP) +
                       " Port " + str(configs.conDNSServerPort) +
                       " Timeout " + str(configs.connTimeOut))
    is_up_last = True  # Pretends the first connection test was UP
    time_since_the_epoch_when_it_was_down = None  # Initialize to avoid flake8 error (F821 undefined name)
    last_error_reason = None  # Initialize to avoid flake8 error (F821 undefined name)
    while (True):
        is_up, error_reason = test_connection_socket(configs.connDNSServerIP, configs.conDNSServerPort, configs.connTimeOut)
        connectionLog.debug("Testing connection... is_up: " + str(is_up) + " is_up_last: " + str(is_up_last))
        if is_up_last == is_up:  # Connection status hasn't changed
            time.sleep(configs.connInterval)
            continue
        if is_up:
            time_since_the_epoch_when_it_turns_up = time.time()
            downtime_in_minutes = get_downtime_in_minutes(time_since_the_epoch_when_it_was_down,
                                                          time_since_the_epoch_when_it_turns_up)
            connectionLog.warning("Internet connection is UP! Downtime: " + str(downtime_in_minutes) + ' minute(s)')
            if configs.notificationEnabled:
                connectionLog.info("Sending notification...")
                notification = SMSNotification(configs.notificationApiKey)
                custom_message = custom_notification_message(last_error_reason, downtime_in_minutes)
                was_sent, response = notification.send_notification(custom_message, configs.notificationPhoneNumber)
                connectionLog.debug("Notification - It was sent?: " + str(was_sent) + " | Response: " + str(response))
                if not was_sent:
                    connectionLog.critical("Notification error: " + str(response))
        else:  # It's down
            time_since_the_epoch_when_it_was_down = time.time()
            last_error_reason = error_reason
            connectionLog.warning("Internet connection is DOWN! Error: " + error_reason)
        is_up_last = is_up
        time.sleep(configs.connInterval)


if __name__ == '__main__':
    main()
