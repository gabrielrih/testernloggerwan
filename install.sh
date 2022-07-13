#!/bin/bash
#
# Install the TesterNLogger
# <gabrielrih>
#

# Is it root?
if [ $(whoami) != root ]; then
    echo -e "Error! Run it as root!"
    exit 1
fi

py_files_handler() {

    # Get destination folder for py files
    DEFAULT_INSTALL_FOLDER="/opt/testerNlogger"
    read -p "[?] Installation folder (default: $DEFAULT_INSTALL_FOLDER): " USER_INSTALL_FOLDER
    if [ $USER_INSTALL_FOLDER ]; then INSTALL_FOLDER=$USER_INSTALL_FOLDER; else INSTALL_FOLDER=$DEFAULT_INSTALL_FOLDER; fi
    timestamp=$(date +%Y%m%d%H%M%S)
    FULL_INSTALL_FOLDER=$INSTALL_FOLDER"-"$timestamp

    # Copying py files
    echo "[+] Copying files to $FULL_INSTALL_FOLDER"
    if [ ! -d $FULL_INSTALL_FOLDER ]; then mkdir -p $FULL_INSTALL_FOLDER; fi
    cp testerNlogger.py $FULL_INSTALL_FOLDER
    cp -R ./libs $FULL_INSTALL_FOLDER/libs
    chmod 744 $FULL_INSTALL_FOLDER/testerNlogger.py

    # Symbolic link for the install folder
    echo "[+] Creating symbolic link for instalation folder..."
    if [ -L $INSTALL_FOLDER ]; then rm $INSTALL_FOLDER; fi
    ln -s $FULL_INSTALL_FOLDER $INSTALL_FOLDER 
}

config_file_handler() {

    # Get destination folder for config file
    DEFAULT_CONFIG_FOLDER="/etc/testerNlogger"
    read -p "[?] Configuration folder (default: $DEFAULT_CONFIG_FOLDER): " USER_CONFIG_FOLDER
    if [ $USER_CONFIG_FOLDER ]; then CONFIG_FOLDER=$USER_CONFIG_FOLDER; else CONFIG_FOLDER=$DEFAULT_CONFIG_FOLDER; fi

    # Copying configuration file
    echo "[+] Copying config file to $CONFIG_FOLDER"
    if [ ! -d $CONFIG_FOLDER ]; then mkdir -p $CONFIG_FOLDER; fi
    cp ./config/config-example.ini $CONFIG_FOLDER/config.ini
}

log_handler() {
    
    # Get destination folder for log files
    DEFAULT_LOG_FOLDER="/var/log/testerNlogger"
    read -p "[?] Log folder (default: $DEFAULT_LOG_FOLDER): " USER_LOG_FOLDER
    if [ $USER_LOG_FOLDER ]; then LOG_FOLDER=$USER_LOG_FOLDER; else LOG_FOLDER=$DEFAULT_LOG_FOLDER; fi

    # Creating log folder
    if [ ! -d $LOG_FOLDER ]
    then
        echo "(+) Creating log folder $LOG_FOLDER"
        mkdir -p $LOG_FOLDER
    fi

    # Replace variable values in config file
    REPLACED_VALUE=$(echo $LOG_FOLDER | sed -e 's/\//\\\//g')
    sed -i "s/\/var\/log\/testerNlogger\//${REPLACED_VALUE}/g" $CONFIG_FOLDER/config.ini
}

service() {
    echo "(+) Configuring service (not implemented yet)..."
    # Do nothing yet
}

echo "Starting TesterNLogger instalation..."
py_files_handler
config_file_handler
log_handler
service
echo "It's done!"