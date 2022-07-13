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

rm -r /var/log/testerNlogger
rm -r /etc/testerNlogger
rm -r /opt/testerNlogger
rm /opt/testerNlogger
rm -r /opt/testerNlogger*