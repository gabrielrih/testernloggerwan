# Reference: https://docs.python.org/3/library/logging.html
import logging
import os


def start_logger(folder, filename, enableDebugMode = False):
    _create_folder(folder)
    fullPath = _mount_fullpath(folder, filename)
    # Configuring logger
    logging.basicConfig(filename=fullPath,
                        format='%(asctime)s %(levelname)s %(message)s',
                        filemode='a')
    # Creating logger
    connectionLog = logging.getLogger()
    if enableDebugMode == 'True':
        connectionLog.setLevel(logging.DEBUG)
    else:
        connectionLog.setLevel(logging.INFO)
    return connectionLog


def clear_logs(folder, filename):
    # Do nothing yet
    return True


def _create_folder(folder):
    if not os.path.exists(folder):
        os.mkdir(folder)


def _mount_fullpath(folder, filename):
    return folder + '/' + filename