#!/bin/bash
#
# Install the TesterNLogger
# By gabrielrih <gabrielrih@gmail.com>
#

VERSION="1.1.0"
INSTALL_FOLDER="/opt/testernlogger"
SERVICE_TEMPLATE_FILENAME="testernlogger.service"

# Is it root?
if [ $(whoami) != root ]; then
    echo -e "Error! Run it as root!"
    exit 1
fi

# Copy script to install folder
echo "[+] Copying files to install folder..."
FULL_INSTALL_FOLDER=$INSTALL_FOLDER"-"$VERSION
if [ ! -d $FULL_INSTALL_FOLDER ]; then mkdir $FULL_INSTALL_FOLDER; fi
cp -R ./testerNlogger $INSTALL_FOLDER
cp -R ./service $INSTALL_FOLDER

# Symbolic link
echo "[+] Creating symbolic link..."
symbolicLinkIsCreated=$(ls /etc/systemd/system | grep $SERVICE_TEMPLATE_FILENAME | wc -l)
if [ $symbolicLinkIsCreated -eq 1 ]; then rm /etc/systemd/system/$SERVICE_TEMPLATE_FILENAME; fi
ln -s $INSTALL_FOLDER/$SERVICE_TEMPLATE_FILENAME /etc/systemd/system/$SERVICE_TEMPLATE_FILENAME

# Service
echo "[+] Configuring service..."
systemctl daemon-reload
systemctl start $SERVICE_TEMPLATE_FILENAME
systemctl enable $SERVICE_TEMPLATE_FILENAME
systemctl status $SERVICE_TEMPLATE_FILENAME

echo "[+] Installed!"

exit 0
