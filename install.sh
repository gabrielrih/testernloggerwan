#!/bin/bash
#
# Install the TesterNLogger
#
# References:
#   https://www.shubhamdipt.com/blog/how-to-create-a-systemd-service-in-linux/
#   https://stackoverflow.com/questions/35984151/how-to-create-new-system-service-by-ansible-playbook
#
# By gabrielrih <gabrielrih@gmail.com>
#

VERSION="1.1.0"
INSTALL_FOLDER="/opt/testerNlogger"
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
cp -R ./testerNlogger/run.sh $FULL_INSTALL_FOLDER
cp -R ./service $FULL_INSTALL_FOLDER

# Symbolic link for the install folder
echo "[+] Creating symbolic link for install folder..."
if [ -L $INSTALL_FOLDER ]; then rm $INSTALL_FOLDER; fi
ln -s $FULL_INSTALL_FOLDER $INSTALL_FOLDER 

# Symbolic link for the service
echo "[+] Creating symbolic link for the service..."
if [ -L /etc/systemd/system/$SERVICE_TEMPLATE_FILENAME ]; then rm /etc/systemd/system/$SERVICE_TEMPLATE_FILENAME; fi
ln -s $INSTALL_FOLDER/service/$SERVICE_TEMPLATE_FILENAME /etc/systemd/system/$SERVICE_TEMPLATE_FILENAME

# Service
echo "[+] Configuring service..."
systemctl daemon-reload
systemctl start $SERVICE_TEMPLATE_FILENAME
systemctl enable $SERVICE_TEMPLATE_FILENAME
systemctl status $SERVICE_TEMPLATE_FILENAME

echo "[+] Installed!"

exit 0
