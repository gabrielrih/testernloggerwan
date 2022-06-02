#!/bin/bash
#
# Tester N Logger
# It tests and it logs the wan connection status.
# By gabrielrih <gabrielrih@gmail.com>
#

# Interval configurations
INTERVAL_TO_TEST_CONNECTION_IN_SECONDS=60

# Debugging and testing configurations
IS_TO_SAVE_DETAIL_LOGS=false
CLEAR_ALL_LOG_FILES_EVERY_START=false
IS_TO_PRINT_LOG_IN_STDOUT=false

# File and folders configurations
LOG_FOLDER="/var/log/testerNlogger"
LOG_FILENAME="connection.log" # in runtime this name is changed
LOG_WHEN_CHANGE_FILENAME="changeHistory.log"
TMP_FOLDER="/tmp/testerNlogger" # used for creating temporary files

# Do not change it
LOG_FULL_PATH=$LOG_FOLDER/$LOG_FILENAME
LOG_ON_CHANGE_FULL_PATH=$LOG_FOLDER/$LOG_WHEN_CHANGE_FILENAME

# Is it root?
if [ $(whoami) != root ]; then
    echo -e "Error! Run it as root!"
    exit 1
fi

testConnection() {
    if [ ! -d $TMP_FOLDER ]; then mkdir $TMP_FOLDER; fi
    ping 8.8.8.8 -c 1 > $TMP_FOLDER/.result.tmp
    checkIfConnectionIsDown
    if [ $isDown -eq 1 ]; then ping 1.1.1.1 -c 1 > $TMP_FOLDER/.result.tmp; fi
    checkIfConnectionIsDown
    return $isDown
}

checkIfConnectionIsDown() {
    isDown=$(cat $TMP_FOLDER/.result.tmp | grep "100% packet loss" | wc -l)
    return $isDown
}

createLogContent() {
    currentDate=$(date +%Y-%m-%d)
    currentTime=$(date +%H:%M:%S)
    if [ $isDown -eq 1 ]; then status='down'; else status='up'; fi
    logContent="$currentDate|$currentTime|$status|" # Format: date|time|status|
}

logWhenStatusChanged() {
    if [ ! $isDownLast ]; then isDownLast=2; fi # first execution. Force value two to print changed log
    if [ ! -f $LOG_ON_CHANGE_FULL_PATH ]; then echo "date|time|status|" >> $LOG_ON_CHANGE_FULL_PATH; fi # print header if log file doesn't exists
    if [ $isDown -ne $isDownLast ]; then echo $logContent >> $LOG_ON_CHANGE_FULL_PATH; fi # it saves the log when status changed
    isDownLast=$isDown # set current as last
}

logEverything() {
    logFullPathWithDate=$(echo $LOG_FULL_PATH | sed "s/\.log/-$currentDate.log/g") # add date in log filename
    if [ ! -f $logFullPathWithDate ]; then echo "date|time|status|" >> $logFullPathWithDate; fi # print header if log file doesn't exists
    echo $logContent >> $logFullPathWithDate # it saves the log
}

# standard stdout
printInStdout() {
    currentDatetime=$currentDate"T"$currentTime
    if [ $isDown -eq 1 ]; then echo "[-] Connection is DOWN! ($currentDatetime)"; else echo "[+] Connection is UP! ($currentDatetime)"; fi
}

cleaningLogFiles() {
    echo "[!] Deleting all log files!"
    if [ -d $LOG_FOLDER ]; then rm -r $LOG_FOLDER; fi
}

echo "Testing WAN connection every $INTERVAL_TO_TEST_CONNECTION_IN_SECONDS seconds..."
if [ $CLEAR_ALL_LOG_FILES_EVERY_START == true ]; then cleaningLogFiles; fi
while true
do
    testConnection
    if [ ! -d $LOG_FOLDER ]; then mkdir $LOG_FOLDER; fi
    createLogContent
    logWhenStatusChanged
    if [ $IS_TO_SAVE_DETAIL_LOGS == true ]; then logEverything; fi
    if [ $IS_TO_PRINT_LOG_IN_STDOUT == true ]; then printInStdout; fi
    sleep $INTERVAL_TO_TEST_CONNECTION_IN_SECONDS
done

exit 0
