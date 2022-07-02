#!/bin/bash
#
# Install the TesterNLogger
#
# References:
#   https://www.shubhamdipt.com/blog/how-to-create-a-systemd-service-in-linux/
# By gabrielrih <gabrielrih@gmail.com>
#

# Is it root?
if [ $(whoami) != root ]; then
    echo -e "Error! Run it as root!"
    exit 1
fi

# Repo version
VERSION="1.2.0"

# Installation configurations
INSTALL_FOLDER="/opt/testerNlogger"
SERVICE_TEMPLATE_FILENAME="testernlogger.service"

# Do not change it
FULL_INSTALL_FOLDER=$INSTALL_FOLDER"-"$VERSION

installation() {

    # Copy script to install folder
    echo "[+] Copying files to install folder..."
    if [ ! -d $FULL_INSTALL_FOLDER ]; then mkdir $FULL_INSTALL_FOLDER; fi
    cp -R ./run.sh $FULL_INSTALL_FOLDER
    if [ ! -d "$FULL_INSTALL_FOLDER/config" ]; then mkdir "$FULL_INSTALL_FOLDER/config"; fi
    cp -R ./config/testerNlogger.conf $FULL_INSTALL_FOLDER/config/testerNlogger.conf
    cp -R ./config/callMeBotConfig.conf $FULL_INSTALL_FOLDER/config/callMeBotConfig.conf # this file is modified next in this same script
    cp -R ./service/$SERVICE_TEMPLATE_FILENAME $FULL_INSTALL_FOLDER
    chmod 744 $FULL_INSTALL_FOLDER/run.sh

    # Symbolic link for the install folder
    echo "[+] Creating symbolic link for install folder..."
    if [ -L $INSTALL_FOLDER ]; then rm $INSTALL_FOLDER; fi
    ln -s $FULL_INSTALL_FOLDER $INSTALL_FOLDER 
}

installationLibraries() {

    echo "[+] Starting libraries installation..."

    # Libraries default folder
    LIBRARIES_INSTALL_FOLDER="$INSTALL_FOLDER/libraries"
    if [ ! -d $LIBRARIES_INSTALL_FOLDER ]; then mkdir $LIBRARIES_INSTALL_FOLDER; fi

    # Install CallMeBot SendNotification library
    callMeBot
}

callMeBot() {

    # Configurations
    CALLMEBOT_VERSION="0.0.4"
    CALLMEBOT_TMP_FOLDER="/tmp/callMeBot"
    CALLMEBOT_INSTALL_FOLDER="$LIBRARIES_INSTALL_FOLDER/callMeBot"
    
    # Get config folder from user
    DEFAULT_CALLMEBOT_CONFIG_FOLDER="/etc/callMeBot"
    read -p "CALLMEBOT_CONFIG_FOLDER (default: $DEFAULT_CALLMEBOT_CONFIG_FOLDER): " USER_CALLMEBOT_CONFIG_FOLDER
    if [ $USER_CALLMEBOT_CONFIG_FOLDER ]; then CALLMEBOT_CONFIG_FOLDER=$USER_CALLMEBOT_CONFIG_FOLDER; else CALLMEBOT_CONFIG_FOLDER=$DEFAULT_CALLMEBOT_CONFIG_FOLDER; fi

    # Download and unzip repo
    echo "[+] Downloading CallMeBot library..."
    wget https://github.com/gabrielrih/callMeBot/archive/refs/tags/$CALLMEBOT_VERSION.tar.gz -P $CALLMEBOT_TMP_FOLDER
    tar -xzvf $CALLMEBOT_TMP_FOLDER/$CALLMEBOT_VERSION.tar.gz -C $CALLMEBOT_TMP_FOLDER

    # Copying library files to TesterNLogger installation folder
    echo "[+] Copying CallMeBot library files..."
    if [ -d $CALLMEBOT_INSTALL_FOLDER ]; then rm -r $CALLMEBOT_INSTALL_FOLDER; fi
    cp -R "$CALLMEBOT_TMP_FOLDER/callMeBot-$CALLMEBOT_VERSION/callMeBot/" "$CALLMEBOT_INSTALL_FOLDER"

    # Copying default config file
    # FIX IT: Perguntar se quer substituir o arquivo atual
    echo "[+] Copying CallMeBot configuration file to '$CALLMEBOT_CONFIG_FOLDER'..."
    if [ ! -d $CALLMEBOT_CONFIG_FOLDER ]; then mkdir $CALLMEBOT_CONFIG_FOLDER; fi
    cp "$CALLMEBOT_TMP_FOLDER/callMeBot-$CALLMEBOT_VERSION/config/credentials-example.yml" "$CALLMEBOT_CONFIG_FOLDER/credentials.yml"

    # Change callMeBotoConfig.conf to point for the right credential file
    # FIX IT: Now this have a fixed value. Change it.
    sudo sed -i 's/.\/config\/callMeBotCredential.yml/\/etc\/callMeBot\/credentials.yml/g' $FULL_INSTALL_FOLDER/config/callMeBotConfig.conf

    # Cleaning up
    echo "[+] Cleaning up CallMeBot temporary folder..."
    rm -r $CALLMEBOT_TMP_FOLDER
}

service() {

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
}

installation
installationLibraries
service

echo "[+] Everything installed!"

exit 0
