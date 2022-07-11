import config
import sys

config = config.Config("config/config.ini")
config.read_configs()
config.get_configs()
print(config.logDefaultFolder)
print(config.logDefaultFilename)
print(config.logClearFilesOnStart)
print(config.logDebugEnabled)
print(config.connInterval)
print(config.connDNSServerIP)
print(config.connDNSServerIP)
print(config.connTimeOut)
print(config.notificationEnabled)
print(config.notificationPhoneNumber)
print(config.notificationApiKey)
print(config.notificationDebugEnabled)