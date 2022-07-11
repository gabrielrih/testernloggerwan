import argparse


def get_arguments():
    parser = argparse.ArgumentParser(description='TesterNLogger WAN connection. It tests the connection and log it every time the connection status changed.')
    parser.add_argument('--config', '-c', help='Configuration file', required=True)
    parser.add_argument('--debug', help='Enabled debug mode', action="store_true")
    args = parser.parse_args()
    if args.debug:
        debugEnabled = True
    else:
        debugEnabled = False
    configFileName = args.config
    return configFileName, debugEnabled