"""
    This methods are used for start a manage a Log file.
    Reference: https://docs.python.org/3/library/logging.html
    <gabrielrih>
"""
import logging
import os

from logging.handlers import RotatingFileHandler
from logging import Formatter

def start_logger(folder,
                 filename,
                 rotationMaxBytesSize,
                 rotationMaxNumberOfFiles,
                 enableDebugMode = False
                ):
    _create_folder(folder)
    connectionLog = logging.getLogger()
    connectionLog.setLevel(logging.INFO)
    if enableDebugMode == True:
        connectionLog.setLevel(logging.DEBUG)
    # It's needed for rotating logs. Reference: https://www.blog.pythonlibrary.org/2014/02/11/python-how-to-create-rotating-logs/   
    fullPath = _mount_fullpath(folder, filename)
    handler = RotatingFileHandler(fullPath, maxBytes=rotationMaxBytesSize, backupCount=rotationMaxNumberOfFiles)
    log_file_format = "%(asctime)s %(levelname)s %(message)s"
    handler.setFormatter(Formatter(log_file_format))
    connectionLog.addHandler(handler)
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