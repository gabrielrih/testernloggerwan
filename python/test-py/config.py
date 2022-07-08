# Reference: https://docs.python.org/3/library/configparser.html
import configparser

def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config

config = read_config()
print(config['groupone']['configone'])
print(config['groupone']['configtwo'])