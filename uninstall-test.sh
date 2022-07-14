#!/bin/bash
#
# Uninstall the TesterNLogger
# <gabrielrih>
#

# Is it root?
if [ $(whoami) != root ]; then
    echo -e "Error! Run it as root!"
    exit 1
fi

# Configurations
APPLICATION_NAME="testerNlogger"
SERVICE_TEMPLATE_FILENAME="testernlogger.service"

# Remove files
rm -r /var/log/$APPLICATION_NAME
rm -r /etc/$APPLICATION_NAME
rm -r /opt/$APPLICATION_NAME
rm /opt/$APPLICATION_NAME
rm -r /opt/$APPLICATION_NAME*

# Remove service
systemctl stop $SERVICE_TEMPLATE_FILENAME
systemctl disable $SERVICE_TEMPLATE_FILENAME