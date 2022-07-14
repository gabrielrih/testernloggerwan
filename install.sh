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

#Configurations
APPLICATION_NAME="testerNlogger"

py_files_handler() {

    # Get destination folder for py files
    DEFAULT_INSTALL_FOLDER="/opt"
    read -p "[?] Installation folder (default: $DEFAULT_INSTALL_FOLDER): " USER_INSTALL_FOLDER
    if [ $USER_INSTALL_FOLDER ]; then INSTALL_FOLDER=$USER_INSTALL_FOLDER; else INSTALL_FOLDER=$DEFAULT_INSTALL_FOLDER; fi
    
    # Set full path for instalation folder
    INSTALL_FOLDER="$INSTALL_FOLDER/$APPLICATION_NAME"
    timestamp=$(date +%Y%m%d%H%M%S)
    FULL_INSTALL_FOLDER=$INSTALL_FOLDER"-"$timestamp

    # Copying py files
    echo "[+] Copying files to $INSTALL_FOLDER"
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
    DEFAULT_CONFIG_FOLDER="/etc"
    read -p "[?] Configuration folder (default: $DEFAULT_CONFIG_FOLDER): " USER_CONFIG_FOLDER
    if [ $USER_CONFIG_FOLDER ]; then CONFIG_FOLDER=$USER_CONFIG_FOLDER; else CONFIG_FOLDER=$DEFAULT_CONFIG_FOLDER; fi

    # Set full path for config folder
    CONFIG_FOLDER="$CONFIG_FOLDER/$APPLICATION_NAME"

    # If config file exists, ask if user wants to replace it
    CONFIG_FILE_DESTINATION_FULL_NAME=$CONFIG_FOLDER/config.ini
    if [ -f $CONFIG_FILE_DESTINATION_FULL_NAME ] # config file already exists
    then
        read -p "[?] File '$CONFIG_FILE_DESTINATION_FULL_NAME' already exists. Do you want to replace it? (Default: N) " answer
        case $answer in
            Y | y | YES | yes ) IS_TO_REPLACE_IT=true;;
            * ) IS_TO_REPLACE_IT=false;;
        esac
    else # force copy when config file doesn't exists
        IS_TO_REPLACE_IT=true
    fi
    if [[ $IS_TO_REPLACE_IT == true ]]; then
        # Copying configuration file
        echo "[+] Copying config file to $CONFIG_FOLDER"
        if [ ! -d $CONFIG_FOLDER ]; then mkdir -p $CONFIG_FOLDER; fi
        cp ./config/config-example.ini $CONFIG_FILE_DESTINATION_FULL_NAME
    fi
}

log_handler() {
    
    # Get destination folder for log files
    DEFAULT_LOG_FOLDER="/var/log"
    read -p "[?] Log folder (default: $DEFAULT_LOG_FOLDER): " USER_LOG_FOLDER
    if [ $USER_LOG_FOLDER ]; then LOG_FOLDER=$USER_LOG_FOLDER; else LOG_FOLDER=$DEFAULT_LOG_FOLDER; fi

    # Set full path for log folder
    LOG_FOLDER="$LOG_FOLDER/$APPLICATION_NAME"

    # Creating log folder
    if [ ! -d $LOG_FOLDER ]
    then
        echo "[+] Creating log folder $LOG_FOLDER"
        mkdir -p $LOG_FOLDER
    fi

    # Replace variable for LOG FOLDER in config file
    echo "[+] Replacing varibles in config file"
    REPLACED_VALUE=$(echo $LOG_FOLDER | sed -e 's/\//\\\//g')
    sed -i "s/\/var\/log\/testerNlogger\//${REPLACED_VALUE}/g" $CONFIG_FOLDER/config.ini
}

service() {
    
    echo "[+] Copying service file to $INSTALL_FOLDER"
    SERVICE_TEMPLATE_FILENAME="testernlogger.service"
    if [ ! -d $FULL_INSTALL_FOLDER/service ]; then mkdir -p $FULL_INSTALL_FOLDER/service; fi
    cp ./service/$SERVICE_TEMPLATE_FILENAME $FULL_INSTALL_FOLDER/service/$SERVICE_TEMPLATE_FILENAME

    # Replace variable value for:
    #   WorkingDirectory in service file
    #   ExecStart in service file
    echo "[+] Replacing varibles in service file"
    REPLACED_VALUE=$(echo $INSTALL_FOLDER | sed -e 's/\//\\\//g')
    sed -i "s/\/opt\/testerNlogger/${REPLACED_VALUE}/g" $FULL_INSTALL_FOLDER/service/$SERVICE_TEMPLATE_FILENAME
    REPLACED_VALUE=$(echo $CONFIG_FOLDER | sed -e 's/\//\\\//g')
    sed -i "s/\/etc\/testerNlogger/${REPLACED_VALUE}/g" $FULL_INSTALL_FOLDER/service/$SERVICE_TEMPLATE_FILENAME

    # Stopping and disable service (if it was already created earlier)
    # FIX IT: Check if the service exists
    echo "[+] Removing service..."
    serviceExists=$(systemctl list-units --full -all | grep "$SERVICE_TEMPLATE_FILENAME" | wc -l)
    if [ $serviceExists -eq 1 ]; then # the service already exists, so stop and disable it
        systemctl daemon-reload
        systemctl stop $SERVICE_TEMPLATE_FILENAME
        systemctl disable $SERVICE_TEMPLATE_FILENAME
        systemctl daemon-reload
    fi

    # Symbolic link for the service
    echo "[+] Creating symbolic link for the service..."
    if [ -L /etc/systemd/system/$SERVICE_TEMPLATE_FILENAME ]; then rm /etc/systemd/system/$SERVICE_TEMPLATE_FILENAME; fi
    ln -s $INSTALL_FOLDER/service/$SERVICE_TEMPLATE_FILENAME /etc/systemd/system/$SERVICE_TEMPLATE_FILENAME

    # Starting service
    echo "[+] Configuring service..."
    systemctl enable $SERVICE_TEMPLATE_FILENAME
    systemctl daemon-reload
    systemctl start $SERVICE_TEMPLATE_FILENAME
}

echo "Starting TesterNLogger instalation..."
py_files_handler
config_file_handler
log_handler
service
echo "It's done!"