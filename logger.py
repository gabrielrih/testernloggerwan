# Reference: https://docs.python.org/3/library/logging.html
import logging
import os


def start_logger(folder, filename, enableDebugMode = False):
    _create_folder(folder)
    fullPath = _mount_fullpath(folder, filename)
    logging.basicConfig(filename=fullPath,
                        format='%(asctime)s %(levelname)s %(message)s',
                        filemode='a')
    connectionLog = logging.getLogger()
    if enableDebugMode == True:
        connectionLog.setLevel(logging.DEBUG)
    else:
        connectionLog.setLevel(logging.INFO)
    return connectionLog


def clear_logs(folder, filename):
    fullPath = _mount_fullpath(folder, filename)
    if os.path.exists(fullPath):
        os.remove(fullPath)


def _create_folder(folder):
    if not os.path.exists(folder):
        os.mkdir(folder)


def _mount_fullpath(folder, filename):
    return folder + '/' + filename