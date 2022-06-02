#!/bin/bash
#
# Install the TesterNLogger
#
# References:
#   https://www.shubhamdipt.com/blog/how-to-create-a-systemd-service-in-linux/
# By gabrielrih <gabrielrih@gmail.com>
#

VERSION="1.1.1"

# Installation configurations
INSTALL_FOLDER="/opt/testerNlogger"
SERVICE_TEMPLATE_FILENAME="testernlogger.service"

# Do not change it
FULL_INSTALL_FOLDER=$INSTALL_FOLDER"-"$VERSION

# Is it root?
if [ $(whoami) != root ]; then
    echo -e "Error! Run it as root!"
    exit 1
fi

# Copy script to install folder
echo "[+] Copying files to install folder..."
if [ ! -d $FULL_INSTALL_FOLDER ]; then mkdir $FULL_INSTALL_FOLDER; fi
cp -R ./testerNlogger/run.sh $FULL_INSTALL_FOLDER
cp -R ./service/$SERVICE_TEMPLATE_FILENAME $FULL_INSTALL_FOLDER
chmod 744 $FULL_INSTALL_FOLDER/run.sh

# Symbolic link for the install folder
echo "[+] Creating symbolic link for install folder..."
if [ -L $INSTALL_FOLDER ]; then rm $INSTALL_FOLDER; fi
ln -s $FULL_INSTALL_FOLDER $INSTALL_FOLDER 

# Stopping and disable service (if it was already created earlier)
echo "[+] Removing service..."
systemctl stop $SERVICE_TEMPLATE_FILENAME
systemctl disable $SERVICE_TEMPLATE_FILENAME

# Symbolic link for the service
echo "[+] Creating symbolic link for the service..."
if [ -L /etc/systemd/system/$SERVICE_TEMPLATE_FILENAME ]; then rm /etc/systemd/system/$SERVICE_TEMPLATE_FILENAME; fi
ln -s $INSTALL_FOLDER/$SERVICE_TEMPLATE_FILENAME /etc/systemd/system/$SERVICE_TEMPLATE_FILENAME

# Starting service
echo "[+] Configuring service..."
systemctl daemon-reload
systemctl start $SERVICE_TEMPLATE_FILENAME
systemctl enable $SERVICE_TEMPLATE_FILENAME
systemctl status $SERVICE_TEMPLATE_FILENAME

echo "[+] Installed!"

exit 0
