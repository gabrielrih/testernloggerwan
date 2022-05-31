#!/bin/bash
#
# Tester N Logger
# It test and log the wan connection status.
# By gabrielrih <gabrielrih@gmail.com>
#

INTERVAL_TO_TEST_CONNECTION_IN_SECONDS=2
LOG_FOLDER="/var/log/testerNlogger"
LOG_FILENAME="connection.log" # in runtime this name is changed
LOG_WHEN_CHANGE_FILENAME="changeHistory.log"
CLEAR_ALL_LOG_FILES_EVERY_START=false
LOG_FULL_PATH=$LOG_FOLDER/$LOG_FILENAME
LOG_ON_CHANGE_FULL_PATH=$LOG_FOLDER/$LOG_WHEN_CHANGE_FILENAME

# Is it root?
if [ $(whoami) != root ]; then
    echo -e "Error! Run it as root!"
    exit 1
fi

testConnection() {
    ping 8.8.8.8 -c 1 > .result.tmp
    isDown=$(cat .result.tmp | grep "100% packet loss" | wc -l)
    return $isDown
}

createLogContent() {
    if [ $isDown -eq 1 ]; then status='down'; else status='up'; fi
    logContent="$currentDate|$currentTime|$status|"
}

logWhenStatusChanged() {
    if [ ! $isDownLast ]; then isDownLast=2; fi # first execution. Force value two to print changed log
    # log file. Format: date|time|status|
    if [ ! -f $LOG_ON_CHANGE_FULL_PATH ]; then echo "date|time|status|" >> $LOG_ON_CHANGE_FULL_PATH; fi # print header if log file doesn't exists
    if [ $isDown -ne $isDownLast ]; then echo $logContent >> $LOG_ON_CHANGE_FULL_PATH; fi
    # set current as last
    isDownLast=$isDown
}

logEverything() {
    # standard stdout
    currentDatetime=$currentDate"T"$currentTime
    if [ $isDown -eq 1 ]; then echo "[-] Connection is DOWN! ($currentDatetime)"; else echo "[+] Connection is UP! ($currentDatetime)"; fi
    # log file. Format: date|time|status|
    logFullPathWithDate=$(echo $LOG_FULL_PATH | sed "s/\.log/-$currentDate.log/g")
    if [ ! -f $logFullPathWithDate ]; then echo "date|time|status|" >> $logFullPathWithDate; fi # print header if log file doesn't exists
    echo $logContent >> $logFullPathWithDate
}

cleaningLogFiles() {
    echo "[!] Deleting all log files!"
    rm -r $LOG_FOLDER
}

echo "Testing WAN connection every $INTERVAL_TO_TEST_CONNECTION_IN_SECONDS seconds..."
if [ $CLEAR_ALL_LOG_FILES_EVERY_START == true ]; then cleaningLogFiles; fi
while true
do
    currentDate=$(date +%Y-%m-%d)
    currentTime=$(date +%H:%M:%S)
    testConnection
    if [ ! -d $LOG_FOLDER ]; then mkdir $LOG_FOLDER; fi
    createLogContent
    logWhenStatusChanged
    logEverything
    sleep $INTERVAL_TO_TEST_CONNECTION_IN_SECONDS
done

exit 0