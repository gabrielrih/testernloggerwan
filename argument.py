import argparse


def get_arguments():
    parser = argparse.ArgumentParser(description='TesterNLogger WAN connection. It tests the connection and log it every time the connection status changed.')
    parser.add_argument('--config', '-c', help='Configuration file', required=True)
    args = parser.parse_args()
    configFileName = args.config
    return configFileName