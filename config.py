# Reference: https://docs.python.org/3/library/configparser.html
import configparser
from os.path import exists

def read_config(path):
    try:    
        if not exists(path):
            error = "ERROR: Config file wasn't found! Check if the config file exists and if it has the right name."
            return None, error
        config = configparser.ConfigParser()
        config.read(path)
        return config, None
    except Exception as error:
        return None, error