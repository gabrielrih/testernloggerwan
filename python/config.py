# Reference: https://docs.python.org/3/library/configparser.html
import configparser

CONFIG_FILENAME = 'config.ini'

def read_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILENAME)
    return config